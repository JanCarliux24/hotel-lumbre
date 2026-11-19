package com.lumbre.hotel.data.firebase

import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.request.delete
import io.ktor.client.request.get
import io.ktor.client.request.header
import io.ktor.client.request.patch
import io.ktor.client.request.post
import io.ktor.client.request.setBody
import io.ktor.client.statement.HttpResponse
import io.ktor.client.statement.bodyAsText
import io.ktor.http.ContentType
import io.ktor.http.HttpStatusCode
import io.ktor.http.contentType
import io.ktor.http.encodeURLParameter
import io.ktor.http.isSuccess
import io.ktor.serialization.kotlinx.json.json
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.JsonNull
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.buildJsonArray
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.put
import kotlinx.serialization.json.putJsonArray
import kotlinx.serialization.json.putJsonObject

/** Error devuelto por Firebase; [code] es el código de la API (p. ej. EMAIL_EXISTS o PERMISSION_DENIED). */
class FirebaseException(val code: String, val status: Int = 0) : Exception(code)

internal val firebaseJson = Json { ignoreUnknownKeys = true; explicitNulls = false }

internal val http: HttpClient by lazy {
    HttpClient { install(ContentNegotiation) { json(firebaseJson) } }
}

private suspend fun HttpResponse.ensureOk(): HttpResponse {
    if (status.isSuccess()) return this
    val text = runCatching { bodyAsText() }.getOrDefault("")
    val code = runCatching {
        val err = firebaseJson.parseToJsonElement(text).jsonObject["error"]?.jsonObject
        err?.get("message")?.jsonPrimitive?.contentOrNull ?: err?.get("status")?.jsonPrimitive?.contentOrNull
    }.getOrNull() ?: "HTTP_${status.value}"
    throw FirebaseException(code.substringBefore(" ").substringBefore(":"), status.value)
}

// ---------------------------------------------------------------------------------------------
// Authentication (Identity Toolkit REST): correo y contraseña.
// ---------------------------------------------------------------------------------------------

data class AuthTokens(val uid: String, val email: String, val idToken: String, val refreshToken: String, val expiresInSec: Long)

object FirebaseAuthApi {
    private const val BASE = "https://identitytoolkit.googleapis.com/v1/accounts"
    private val key get() = FirebaseConfig.API_KEY

    private suspend fun call(op: String, body: JsonObject): JsonObject =
        http.post("$BASE:$op?key=$key") { contentType(ContentType.Application.Json); setBody(body) }
            .ensureOk().body()

    private fun JsonObject.str(k: String) = this[k]?.jsonPrimitive?.contentOrNull ?: ""

    private fun tokens(o: JsonObject) = AuthTokens(
        uid = o.str("localId"), email = o.str("email"), idToken = o.str("idToken"),
        refreshToken = o.str("refreshToken"), expiresInSec = o.str("expiresIn").toLongOrNull() ?: 3600,
    )

    suspend fun signUp(email: String, password: String) = tokens(call("signUp", buildJsonObject {
        put("email", email); put("password", password); put("returnSecureToken", true)
    }))

    suspend fun signIn(email: String, password: String) = tokens(call("signInWithPassword", buildJsonObject {
        put("email", email); put("password", password); put("returnSecureToken", true)
    }))

    /** Renueva el token de sesión (dura 1 h) con el refresh token guardado. */
    suspend fun refresh(refreshToken: String): AuthTokens {
        val o: JsonObject = http.post("https://securetoken.googleapis.com/v1/token?key=$key") {
            contentType(ContentType.Application.FormUrlEncoded)
            setBody("grant_type=refresh_token&refresh_token=${refreshToken.encodeURLParameter()}")
        }.ensureOk().body()
        return AuthTokens(
            uid = o.str("user_id"), email = "", idToken = o.str("id_token"),
            refreshToken = o.str("refresh_token"), expiresInSec = o.str("expires_in").toLongOrNull() ?: 3600,
        )
    }

    suspend fun sendPasswordReset(email: String) {
        call("sendOobCode", buildJsonObject { put("requestType", "PASSWORD_RESET"); put("email", email) })
    }

    suspend fun sendEmailVerification(idToken: String) {
        call("sendOobCode", buildJsonObject { put("requestType", "VERIFY_EMAIL"); put("idToken", idToken) })
    }

    suspend fun isEmailVerified(idToken: String): Boolean {
        val o = call("lookup", buildJsonObject { put("idToken", idToken) })
        val user = o["users"]?.jsonArray?.firstOrNull()?.jsonObject ?: return false
        return user["emailVerified"]?.jsonPrimitive?.contentOrNull == "true"
    }

    suspend fun changePassword(idToken: String, newPassword: String) = tokens(call("update", buildJsonObject {
        put("idToken", idToken); put("password", newPassword); put("returnSecureToken", true)
    }))

    suspend fun deleteAccount(idToken: String) {
        call("delete", buildJsonObject { put("idToken", idToken) })
    }
}

// ---------------------------------------------------------------------------------------------
// Cloud Firestore (REST). Los documentos se representan como Map<String, Any?>.
// ---------------------------------------------------------------------------------------------

data class FsDoc(val id: String, val fields: Map<String, Any?>)

object FirestoreCodec {
    fun encode(v: Any?): JsonObject = buildJsonObject {
        when (v) {
            null -> put("nullValue", JsonNull)
            is String -> put("stringValue", v)
            is Boolean -> put("booleanValue", v)
            is Int -> put("integerValue", v.toString())
            is Long -> put("integerValue", v.toString())
            is Double -> put("doubleValue", v)
            is Float -> put("doubleValue", v.toDouble())
            is Enum<*> -> put("stringValue", v.name)
            is Collection<*> -> putJsonObject("arrayValue") { putJsonArray("values") { v.forEach { add(encode(it)) } } }
            is Map<*, *> -> putJsonObject("mapValue") { put("fields", encodeFields(v.mapKeys { it.key.toString() })) }
            else -> put("stringValue", v.toString())
        }
    }

    fun encodeFields(fields: Map<String, Any?>): JsonObject = JsonObject(fields.mapValues { encode(it.value) })

    fun decode(v: JsonElement): Any? {
        val o = v.jsonObject
        o["stringValue"]?.let { return it.jsonPrimitive.content }
        o["integerValue"]?.let { return it.jsonPrimitive.content.toLongOrNull() }
        o["doubleValue"]?.let { return it.jsonPrimitive.content.toDoubleOrNull() }
        o["booleanValue"]?.let { return it.jsonPrimitive.content == "true" }
        o["timestampValue"]?.let { return it.jsonPrimitive.content }
        o["arrayValue"]?.let { a -> return a.jsonObject["values"]?.jsonArray?.map { decode(it) } ?: emptyList<Any?>() }
        o["mapValue"]?.let { m -> return decodeFields(m.jsonObject["fields"]?.jsonObject) }
        return null
    }

    fun decodeFields(fields: JsonObject?): Map<String, Any?> = fields?.mapValues { decode(it.value) } ?: emptyMap()

    fun doc(o: JsonObject): FsDoc {
        val name = o["name"]?.jsonPrimitive?.content ?: ""
        return FsDoc(name.substringAfterLast('/'), decodeFields(o["fields"]?.jsonObject))
    }
}

/** Cliente REST de Firestore. [token] devuelve el ID token del usuario (las reglas lo validan). */
class FirestoreApi(private val token: suspend () -> String?) {
    private val base get() = "https://firestore.googleapis.com/v1/projects/${FirebaseConfig.PROJECT_ID}/databases/(default)/documents"

    private suspend fun io.ktor.client.request.HttpRequestBuilder.auth() {
        token()?.let { header("Authorization", "Bearer $it") }
    }

    suspend fun get(path: String): FsDoc? {
        val r = http.get("$base/$path") { auth() }
        if (r.status == HttpStatusCode.NotFound) return null
        return FirestoreCodec.doc(r.ensureOk().body())
    }

    /** Crea o reemplaza el documento completo. */
    suspend fun set(path: String, fields: Map<String, Any?>) {
        http.patch("$base/$path") {
            auth(); contentType(ContentType.Application.Json)
            setBody(buildJsonObject { put("fields", FirestoreCodec.encodeFields(fields)) })
        }.ensureOk()
    }

    /** Actualiza solo los campos indicados. */
    suspend fun update(path: String, fields: Map<String, Any?>) {
        val mask = fields.keys.joinToString("&") { "updateMask.fieldPaths=${it.encodeURLParameter()}" }
        http.patch("$base/$path?$mask&currentDocument.exists=true") {
            auth(); contentType(ContentType.Application.Json)
            setBody(buildJsonObject { put("fields", FirestoreCodec.encodeFields(fields)) })
        }.ensureOk()
    }

    suspend fun delete(path: String) {
        http.delete("$base/$path") { auth() }.ensureOk()
    }

    suspend fun list(collection: String): List<FsDoc> {
        val out = mutableListOf<FsDoc>()
        var page: String? = null
        do {
            val url = "$base/$collection?pageSize=300" + (page?.let { "&pageToken=${it.encodeURLParameter()}" } ?: "")
            val o: JsonObject = http.get(url) { auth() }.ensureOk().body()
            o["documents"]?.jsonArray?.forEach { out += FirestoreCodec.doc(it.jsonObject) }
            page = o["nextPageToken"]?.jsonPrimitive?.contentOrNull
        } while (page != null)
        return out
    }

    /** Consulta con igualdad: where field == value. */
    suspend fun whereEquals(collection: String, field: String, value: Any): List<FsDoc> {
        val body = buildJsonObject {
            putJsonObject("structuredQuery") {
                put("from", buildJsonArray { add(buildJsonObject { put("collectionId", collection) }) })
                putJsonObject("where") {
                    putJsonObject("fieldFilter") {
                        putJsonObject("field") { put("fieldPath", field) }
                        put("op", "EQUAL")
                        put("value", FirestoreCodec.encode(value))
                    }
                }
            }
        }
        val arr: JsonArray = http.post("$base:runQuery") {
            auth(); contentType(ContentType.Application.Json); setBody(body)
        }.ensureOk().body()
        return arr.mapNotNull { el -> el.jsonObject["document"]?.jsonObject?.let { FirestoreCodec.doc(it) } }
    }

    /** Añade un documento con identificador automático. */
    suspend fun add(collection: String, fields: Map<String, Any?>) {
        http.post("$base/$collection") {
            auth(); contentType(ContentType.Application.Json)
            setBody(buildJsonObject { put("fields", FirestoreCodec.encodeFields(fields)) })
        }.ensureOk()
    }
}

internal fun Map<String, Any?>.str(k: String, d: String = "") = (this[k] as? String) ?: d
internal fun Map<String, Any?>.int(k: String, d: Int = 0) = (this[k] as? Number)?.toInt() ?: (this[k] as? String)?.toIntOrNull() ?: d
internal fun Map<String, Any?>.long(k: String, d: Long = 0) = (this[k] as? Number)?.toLong() ?: d
internal fun Map<String, Any?>.dbl(k: String, d: Double = 0.0) = (this[k] as? Number)?.toDouble() ?: d
internal fun Map<String, Any?>.bool(k: String, d: Boolean = false) = (this[k] as? Boolean) ?: d
internal fun Map<String, Any?>.strList(k: String) = (this[k] as? List<*>)?.mapNotNull { it as? String } ?: emptyList()

@Suppress("unused") private val keepPrimitive: JsonPrimitive = JsonPrimitive("")
