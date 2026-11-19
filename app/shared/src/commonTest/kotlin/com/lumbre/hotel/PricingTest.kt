package com.lumbre.hotel

import com.lumbre.hotel.data.Extra
import com.lumbre.hotel.data.Params
import com.lumbre.hotel.data.RoomConfig
import com.lumbre.hotel.data.RoomId
import com.lumbre.hotel.domain.LineKind
import com.lumbre.hotel.domain.Pricing
import kotlinx.datetime.LocalDate
import kotlin.math.abs
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNull
import kotlin.test.assertTrue

class PricingTest {
    private val deluxe = RoomConfig(RoomId.DELUXE, 190, 3)
    private fun near(expected: Double, actual: Double) = assertTrue(abs(expected - actual) < 0.01, "esperado $expected, obtenido $actual")

    @Test
    fun tresNochesEntreSemanaSinExtras() {
        // martes 1 → viernes 4 de diciembre de 2026: noches de martes, miércoles y jueves.
        val q = Pricing.quote(deluxe, LocalDate(2026, 12, 1), LocalDate(2026, 12, 4), 2, 0, emptySet())!!
        assertEquals(3, q.nights)
        near(570.0 + 57.0, q.totalEur) // 3 × 190 + 10 % de impuestos
        assertTrue(q.lines.none { it.kind == LineKind.WEEKEND })
    }

    @Test
    fun recargoDeFinDeSemana() {
        // viernes 4 → domingo 6: noches de viernes y sábado (+15 % cada una).
        val q = Pricing.quote(deluxe, LocalDate(2026, 12, 4), LocalDate(2026, 12, 6), 2, 0, emptySet())!!
        near(57.0, q.lines.first { it.kind == LineKind.WEEKEND }.amountEur)
    }

    @Test
    fun descuentoLargaEstanciaYPromocion() {
        val q = Pricing.quote(deluxe, LocalDate(2026, 12, 1), LocalDate(2026, 12, 8), 2, 0, emptySet(), promoPercent = 10)!!
        assertTrue(q.hasLongStay)
        assertTrue(q.lines.any { it.kind == LineKind.PROMO && it.isDiscount })
    }

    @Test
    fun extrasSegunUnidadDeCobro() {
        val q = Pricing.quote(deluxe, LocalDate(2026, 12, 1), LocalDate(2026, 12, 3), 2, 2, setOf(Extra.BREAKFAST, Extra.SPA, Extra.TRANSFER))!!
        near(18.0 * 2 * (2 + 2 * 0.5), q.lines.first { it.extra == Extra.BREAKFAST }.amountEur) // persona y noche, niños al 50 %
        near(45.0 * 2, q.lines.first { it.extra == Extra.SPA }.amountEur) // por adulto
        near(60.0, q.lines.first { it.extra == Extra.TRANSFER }.amountEur) // por estancia
    }

    @Test
    fun parametrosDelSistemaCambianElCalculo() {
        val params = Params(taxPercent = 0, maxNights = 2)
        assertNull(Pricing.quote(deluxe, LocalDate(2026, 12, 1), LocalDate(2026, 12, 4), 2, 0, emptySet(), params = params))
        val q = Pricing.quote(deluxe, LocalDate(2026, 12, 1), LocalDate(2026, 12, 3), 2, 0, emptySet(), params = params)!!
        near(380.0, q.totalEur)
    }

    @Test
    fun fechasInvalidasDevuelvenNull() {
        assertNull(Pricing.quote(deluxe, LocalDate(2026, 12, 5), LocalDate(2026, 12, 5), 2, 0, emptySet()))
        assertNull(Pricing.quote(deluxe, LocalDate(2026, 12, 5), LocalDate(2026, 12, 1), 2, 0, emptySet()))
    }
}
