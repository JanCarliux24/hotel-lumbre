package com.lumbre.hotel.data.firebase

import com.lumbre.hotel.data.Account
import com.lumbre.hotel.data.AuditEntry
import com.lumbre.hotel.data.Extra
import com.lumbre.hotel.data.Params
import com.lumbre.hotel.data.PromoCode
import com.lumbre.hotel.data.Reservation
import com.lumbre.hotel.data.ReservationStatus
import com.lumbre.hotel.data.Role
import com.lumbre.hotel.data.RoomConfig
import com.lumbre.hotel.data.RoomId
import kotlinx.datetime.LocalDate

/** Conversión entre los modelos de la app y los documentos de Firestore. */
internal object Mappers {

    fun reservationToFields(r: Reservation): Map<String, Any?> = mapOf(
        "ref" to r.ref, "uid" to r.uid, "guestName" to r.guestName, "email" to r.email, "phone" to r.phone,
        "room" to r.room.name, "checkIn" to r.checkIn.toString(), "checkOut" to r.checkOut.toString(),
        "adults" to r.adults, "children" to r.children, "extras" to r.extras.map { it.name },
        "promo" to (r.promo ?: ""), "totalEur" to r.totalEur, "status" to r.status.name,
        "createdAt" to r.createdAt, "notes" to r.notes,
    )

    fun reservation(d: FsDoc, myUid: String?): Reservation? = runCatching {
        val f = d.fields
        Reservation(
            ref = f.str("ref", d.id), guestName = f.str("guestName"), email = f.str("email"), phone = f.str("phone"),
            room = RoomId.valueOf(f.str("room", "DELUXE")),
            checkIn = LocalDate.parse(f.str("checkIn")), checkOut = LocalDate.parse(f.str("checkOut")),
            adults = f.int("adults", 1), children = f.int("children"),
            extras = f.strList("extras").mapNotNull { n -> Extra.entries.firstOrNull { it.name == n } }.toSet(),
            promo = f.str("promo").ifBlank { null }, totalEur = f.dbl("totalEur"),
            status = ReservationStatus.entries.firstOrNull { it.name == f.str("status") } ?: ReservationStatus.CONFIRMED,
            mine = myUid != null && f.str("uid") == myUid, uid = f.str("uid"),
            createdAt = f.long("createdAt"), notes = f.str("notes"),
        )
    }.getOrNull()

    fun roomToFields(r: RoomConfig): Map<String, Any?> =
        mapOf("nightlyEur" to r.nightlyEur, "capacity" to r.capacity, "available" to r.available)

    fun room(d: FsDoc): RoomConfig? = runCatching {
        RoomConfig(RoomId.valueOf(d.id), d.fields.int("nightlyEur", 100), d.fields.int("capacity", 2), d.fields.bool("available", true))
    }.getOrNull()

    fun promoToFields(p: PromoCode): Map<String, Any?> = mapOf("percent" to p.percent, "active" to p.active)

    fun promo(d: FsDoc) = PromoCode(d.id, d.fields.int("percent", 10), d.fields.bool("active", true))

    fun account(d: FsDoc, emailVerified: Boolean = false) = Account(
        uid = d.id, email = d.fields.str("email"), name = d.fields.str("name"), phone = d.fields.str("phone"),
        role = Role.entries.firstOrNull { it.name == d.fields.str("role") } ?: Role.GUEST,
        emailVerified = emailVerified, createdAt = d.fields.long("createdAt"), lastLogin = d.fields.long("lastLogin"),
        disabled = d.fields.bool("disabled"),
    )

    fun paramsToFields(p: Params): Map<String, Any?> = mapOf(
        "taxPercent" to p.taxPercent, "weekendSurchargePercent" to p.weekendSurchargePercent,
        "longStayDiscountPercent" to p.longStayDiscountPercent, "longStayNights" to p.longStayNights,
        "maxNights" to p.maxNights, "maxMonthsAhead" to p.maxMonthsAhead, "bookingCooldownSec" to p.bookingCooldownSec,
        "maxLoginAttempts" to p.maxLoginAttempts, "lockoutSec" to p.lockoutSec, "minPasswordLength" to p.minPasswordLength,
        "maintenance" to p.maintenance, "maintenanceMessage" to p.maintenanceMessage,
    )

    fun params(d: FsDoc): Params {
        val f = d.fields; val def = Params()
        return Params(
            taxPercent = f.int("taxPercent", def.taxPercent),
            weekendSurchargePercent = f.int("weekendSurchargePercent", def.weekendSurchargePercent),
            longStayDiscountPercent = f.int("longStayDiscountPercent", def.longStayDiscountPercent),
            longStayNights = f.int("longStayNights", def.longStayNights),
            maxNights = f.int("maxNights", def.maxNights),
            maxMonthsAhead = f.int("maxMonthsAhead", def.maxMonthsAhead),
            bookingCooldownSec = f.int("bookingCooldownSec", def.bookingCooldownSec),
            maxLoginAttempts = f.int("maxLoginAttempts", def.maxLoginAttempts),
            lockoutSec = f.int("lockoutSec", def.lockoutSec),
            minPasswordLength = f.int("minPasswordLength", def.minPasswordLength),
            maintenance = f.bool("maintenance"), maintenanceMessage = f.str("maintenanceMessage"),
        )
    }

    fun audit(d: FsDoc) = AuditEntry(d.fields.long("at"), d.fields.str("actor"), d.fields.str("action"), d.fields.str("target"))
}
