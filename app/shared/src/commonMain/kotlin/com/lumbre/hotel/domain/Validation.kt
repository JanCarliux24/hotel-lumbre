package com.lumbre.hotel.domain

import com.lumbre.hotel.i18n.K
import kotlinx.datetime.DateTimeUnit
import kotlinx.datetime.LocalDate
import kotlinx.datetime.daysUntil
import kotlinx.datetime.plus

/** Validaciones compartidas. Devuelven la clave del mensaje de error o null si todo es correcto. */
object Validation {
    private const val MAX_MONTHS_AHEAD = 18

    private val emailRegex = Regex(
        "^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?(?:\\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$"
    )
    private val typoDomains = mapOf(
        "gmial.com" to "gmail.com", "gmai.com" to "gmail.com", "gnail.com" to "gmail.com", "gmail.con" to "gmail.com",
        "gmail.co" to "gmail.com", "gmal.com" to "gmail.com", "hotmial.com" to "hotmail.com", "hotmal.com" to "hotmail.com",
        "hotmail.con" to "hotmail.com", "hotmail.co" to "hotmail.com", "outlok.com" to "outlook.com", "outlook.con" to "outlook.com",
        "yaho.com" to "yahoo.com", "yahoo.con" to "yahoo.com", "icloud.con" to "icloud.com",
    )
    private val nameExtraChars = setOf(' ', '\'', '’', '.', '-')

    fun name(value: String): K? {
        val v = value.trim()
        if (v.isEmpty()) return K.E_REQUIRED
        if (v.length !in 2..80 || !v.first().isLetter() || v.any { !it.isLetter() && it !in nameExtraChars }) return K.E_NAME
        return null
    }

    fun email(value: String): K? {
        val v = value.trim()
        if (v.isEmpty()) return K.E_REQUIRED
        val at = v.lastIndexOf('@')
        if (at <= 0 || v.length > 254 || at > 64) return K.E_EMAIL
        val local = v.substring(0, at)
        val tld = v.substringAfterLast('.')
        if (!emailRegex.matches(v) || ".." in v || local.startsWith('.') || local.endsWith('.') ||
            tld.length < 2 || !tld.all { it.isLetter() }
        ) return K.E_EMAIL
        return null
    }

    /** Si el dominio parece una errata conocida (gmial.com…), propone la corrección. */
    fun emailSuggestion(value: String): String? {
        val v = value.trim()
        val at = v.lastIndexOf('@').takeIf { it > 0 } ?: return null
        val fix = typoDomains[v.substring(at + 1).lowercase()] ?: return null
        return v.substring(0, at + 1) + fix
    }

    /** Opcional: vacío es válido. */
    fun phone(value: String): K? {
        val v = value.trim()
        if (v.isEmpty()) return null
        if (!(v.first() == '+' || v.first().isDigit()) || v.any { !it.isDigit() && it !in "+ ().-" }) return K.E_PHONE
        val digits = v.count { it.isDigit() }
        return if (digits in 7..15) null else K.E_PHONE
    }

    fun dates(checkIn: LocalDate?, checkOut: LocalDate?, today: LocalDate): K? {
        if (checkIn == null || checkOut == null) return K.E_PICK_DATES
        if (checkIn < today) return K.E_PAST
        if (checkIn > today.plus(MAX_MONTHS_AHEAD, DateTimeUnit.MONTH)) return K.E_FAR
        if (checkOut <= checkIn) return K.E_ORDER
        if (checkIn.daysUntil(checkOut) > Pricing.MAX_NIGHTS) return K.E_MAXSTAY
        return null
    }

    fun latestBookable(today: LocalDate): LocalDate = today.plus(MAX_MONTHS_AHEAD, DateTimeUnit.MONTH)

    fun promoCode(value: String): K? =
        if (value.length in 4..20 && value.all { it in 'A'..'Z' || it in '0'..'9' }) null else K.E_CODE
}
