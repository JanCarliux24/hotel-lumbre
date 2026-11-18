package com.lumbre.hotel.data

import kotlinx.datetime.LocalDate
import kotlinx.serialization.Serializable

@Serializable
enum class RoomId { STANDARD, DELUXE, PENTHOUSE }

/** Datos editables desde el panel administrativo. */
@Serializable
data class RoomConfig(
    val id: RoomId,
    val nightlyEur: Int,
    val capacity: Int,
    val available: Boolean = true,
)

enum class ExtraUnit { PER_PERSON_NIGHT, PER_ADULT, PER_STAY, PER_NIGHT }

@Serializable
enum class Extra(val eur: Int, val unit: ExtraUnit) {
    BREAKFAST(18, ExtraUnit.PER_PERSON_NIGHT),
    SPA(45, ExtraUnit.PER_ADULT),
    TRANSFER(60, ExtraUnit.PER_STAY),
    PARKING(15, ExtraUnit.PER_NIGHT),
    LATE_CHECKOUT(30, ExtraUnit.PER_STAY),
}

@Serializable
enum class ReservationStatus { CONFIRMED, CHECKED_IN, CANCELLED }

@Serializable
data class Reservation(
    val ref: String,
    val guestName: String,
    val email: String,
    val phone: String = "",
    val room: RoomId,
    val checkIn: LocalDate,
    val checkOut: LocalDate,
    val adults: Int,
    val children: Int,
    val extras: Set<Extra> = emptySet(),
    val promo: String? = null,
    val totalEur: Double,
    val status: ReservationStatus = ReservationStatus.CONFIRMED,
    /** true si la hizo quien usa este dispositivo (aparece en "Mis reservas"). */
    val mine: Boolean = false,
)

@Serializable
data class PromoCode(val code: String, val percent: Int, val active: Boolean = true)

@Serializable
enum class Lang(val code: String, val label: String) {
    ES("es", "Español"), EN("en", "English"), PT("pt", "Português"), FR("fr", "Français")
}

/** Tipos de cambio aproximados, base EUR. */
@Serializable
enum class Currency(val code: String, val symbol: String, val rate: Double) {
    EUR("EUR", "€", 1.0),
    USD("USD", "US$", 1.08),
    MXN("MXN", "MX$", 19.8),
    GBP("GBP", "£", 0.85),
    BRL("BRL", "R$", 6.2),
    COP("COP", "COL$", 4550.0),
}

@Serializable
enum class ThemeMode { LIGHT, DARK, SYSTEM }

@Serializable
data class Prefs(
    val lang: Lang = Lang.ES,
    val currency: Currency = Currency.EUR,
    val region: String? = null,
    val regionNoticeShown: Boolean = false,
    /** Claro por defecto: es un hotel de playa. */
    val theme: ThemeMode = ThemeMode.LIGHT,
    /** Sesión de administrador de demostración (solo se puede activar en la web). */
    val admin: Boolean = false,
)
