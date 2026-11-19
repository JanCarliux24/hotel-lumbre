package com.lumbre.hotel.data.firebase

/**
 * Configuración del proyecto de Firebase (plan Spark, gratuito).
 *
 * La API key web de Firebase es pública por diseño: identifica el proyecto, no da permisos.
 * La seguridad real la imponen las reglas de Firestore (firebase/firestore.rules), que validan
 * el token de sesión y el rol de cada usuario en el servidor.
 *
 * Si se deja vacía, la app funciona en "modo local" (datos solo en el dispositivo).
 */
object FirebaseConfig {
    const val API_KEY: String = "AIzaSyCNRoPxy9EjhXsZnVhT-pZlUvBa36UPZ-k"
    const val PROJECT_ID: String = "lumbre-hotel"

    val enabled: Boolean get() = API_KEY.isNotBlank() && PROJECT_ID.isNotBlank()
}
