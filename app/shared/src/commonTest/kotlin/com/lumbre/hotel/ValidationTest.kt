package com.lumbre.hotel

import com.lumbre.hotel.data.Currency
import com.lumbre.hotel.data.HotelRepository
import com.lumbre.hotel.data.Lang
import com.lumbre.hotel.data.Role
import com.lumbre.hotel.data.firebase.FirestoreCodec
import com.lumbre.hotel.domain.Format
import com.lumbre.hotel.domain.Validation
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.i18n.missingTranslations
import com.lumbre.hotel.platform.roughCountry
import kotlinx.datetime.LocalDate
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNull
import kotlin.test.assertTrue

class ValidationTest {
    @Test
    fun correos() {
        assertNull(Validation.email("ana@gmail.com"))
        assertNull(Validation.email("a.b+reservas@hotel.com.mx"))
        assertEquals(K.E_REQUIRED, Validation.email(""))
        assertEquals(K.E_EMAIL, Validation.email("ana@@x"))
        assertEquals(K.E_EMAIL, Validation.email("ana..p@gmail.com"))
        assertEquals(K.E_EMAIL, Validation.email("ana@gmail.c0m"))
        assertEquals("ana@gmail.com", Validation.emailSuggestion("ana@gmial.com"))
        assertNull(Validation.emailSuggestion("ana@gmail.com"))
    }

    @Test
    fun nombresYTelefonos() {
        assertNull(Validation.name("Ana Pérez"))
        assertNull(Validation.name("O'Connor-Díaz"))
        assertEquals(K.E_NAME, Validation.name("Ana 123"))
        assertNull(Validation.phone(""))
        assertNull(Validation.phone("+52 55 1234 5678"))
        assertEquals(K.E_PHONE, Validation.phone("12"))
        assertEquals(K.E_PHONE, Validation.phone("abc1234567"))
    }

    @Test
    fun politicaDeContrasenas() {
        assertEquals(K.E_PASS_LENGTH, Validation.password("Ab1!", 8))
        assertEquals(K.E_PASS_RULES, Validation.password("abcdefgh1", 8))
        assertEquals(K.E_PASS_EMAIL, Validation.password("Marisol#2026", 8, "marisol@correo.com"))
        assertNull(Validation.password("Playa#Sol2026", 8, "ana@correo.com"))
        assertEquals(K.E_PASS_MATCH, Validation.passwordsMatch("a", "b"))
        assertTrue(Validation.passwordStrength("Playa#Sol2026") >= 3)
        assertEquals(0, Validation.passwordStrength(""))
    }

    @Test
    fun fechas() {
        val hoy = LocalDate(2026, 11, 18)
        assertNull(Validation.dates(LocalDate(2026, 12, 1), LocalDate(2026, 12, 4), hoy))
        assertEquals(K.E_PAST, Validation.dates(LocalDate(2026, 11, 1), LocalDate(2026, 11, 4), hoy))
        assertEquals(K.E_ORDER, Validation.dates(LocalDate(2026, 12, 4), LocalDate(2026, 12, 1), hoy))
        assertEquals(K.E_MAXSTAY, Validation.dates(LocalDate(2026, 12, 1), LocalDate(2027, 2, 1), hoy))
        assertEquals(K.E_FAR, Validation.dates(LocalDate(2028, 12, 1), LocalDate(2028, 12, 3), hoy))
    }

    @Test
    fun formatoDeMoneda() {
        assertEquals("627 €", Format.money(627.0, Currency.EUR, Lang.ES))
        assertEquals("MX$12,415", Format.money(627.0, Currency.MXN, Lang.EN))
        assertEquals("US$677", Format.money(627.0, Currency.USD, Lang.EN))
    }

    @Test
    fun deteccionDeIdiomaYMoneda() {
        val mx = HotelRepository.detectPrefs("es-MX")
        assertEquals(Lang.ES, mx.lang); assertEquals(Currency.MXN, mx.currency); assertEquals("MX", mx.region)
        val us = HotelRepository.detectPrefs("en-US")
        assertEquals(Lang.EN, us.lang); assertEquals(Currency.USD, us.currency)
        assertEquals(Currency.EUR, HotelRepository.detectPrefs("fr-FR").currency)
        assertEquals("MX", roughCountry(19.7, -101.2)) // Morelia
        assertEquals("ES", roughCountry(40.4, -3.7))   // Madrid
    }

    @Test
    fun rolesYTraducciones() {
        assertTrue(Role.SUPERADMIN.atLeast(Role.ADMIN))
        assertFalse(Role.STAFF.atLeast(Role.ADMIN))
        assertTrue(missingTranslations().isEmpty(), "Faltan traducciones: ${missingTranslations()}")
    }

    @Test
    fun codecDeFirestore() {
        val fields = mapOf("a" to "texto", "b" to 3, "c" to 2.5, "d" to true, "e" to listOf("x", "y"), "f" to null)
        val decoded = FirestoreCodec.decodeFields(FirestoreCodec.encodeFields(fields))
        assertEquals("texto", decoded["a"]); assertEquals(3L, decoded["b"]); assertEquals(2.5, decoded["c"])
        assertEquals(true, decoded["d"]); assertEquals(listOf("x", "y"), decoded["e"]); assertNull(decoded["f"])
    }
}
