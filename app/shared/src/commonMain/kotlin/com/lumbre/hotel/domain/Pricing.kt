package com.lumbre.hotel.domain

import com.lumbre.hotel.data.Extra
import com.lumbre.hotel.data.ExtraUnit
import com.lumbre.hotel.data.RoomConfig
import kotlinx.datetime.DateTimeUnit
import kotlinx.datetime.DayOfWeek
import kotlinx.datetime.LocalDate
import kotlinx.datetime.daysUntil
import kotlinx.datetime.plus

enum class LineKind { ROOM, WEEKEND, EXTRA, LONG_STAY, PROMO, TAX }

data class QuoteLine(val kind: LineKind, val amountEur: Double, val extra: Extra? = null, val percent: Int = 0) {
    val isDiscount: Boolean get() = amountEur < 0
}

data class Quote(val nights: Int, val lines: List<QuoteLine>, val totalEur: Double) {
    val perNightEur: Double get() = if (nights > 0) totalEur / nights else 0.0
    val hasLongStay: Boolean get() = lines.any { it.kind == LineKind.LONG_STAY }
}

/** Reglas de precio, idénticas en las tres plataformas (y en la web estática). */
object Pricing {
    const val WEEKEND_SURCHARGE = 0.15
    const val LONG_STAY_DISCOUNT = 0.10
    const val LONG_STAY_NIGHTS = 7
    const val TAX_RATE = 0.10
    const val MAX_NIGHTS = 30

    fun quote(
        room: RoomConfig,
        checkIn: LocalDate,
        checkOut: LocalDate,
        adults: Int,
        children: Int,
        extras: Set<Extra>,
        promoPercent: Int = 0,
    ): Quote? {
        val nights = checkIn.daysUntil(checkOut)
        if (nights !in 1..MAX_NIGHTS) return null

        var base = 0.0
        var weekend = 0.0
        for (i in 0 until nights) {
            val day = checkIn.plus(i, DateTimeUnit.DAY).dayOfWeek
            base += room.nightlyEur
            if (day == DayOfWeek.FRIDAY || day == DayOfWeek.SATURDAY) weekend += room.nightlyEur * WEEKEND_SURCHARGE
        }
        val lines = mutableListOf(QuoteLine(LineKind.ROOM, base))
        if (weekend > 0) lines += QuoteLine(LineKind.WEEKEND, weekend)

        var extrasTotal = 0.0
        for (x in Extra.entries.filter { it in extras }) {
            val amount = when (x.unit) {
                ExtraUnit.PER_PERSON_NIGHT -> x.eur * nights * (adults + children * 0.5)
                ExtraUnit.PER_ADULT -> x.eur.toDouble() * adults
                ExtraUnit.PER_NIGHT -> x.eur.toDouble() * nights
                ExtraUnit.PER_STAY -> x.eur.toDouble()
            }
            extrasTotal += amount
            lines += QuoteLine(LineKind.EXTRA, amount, extra = x)
        }

        val stay = base + weekend
        val longStay = if (nights >= LONG_STAY_NIGHTS) -stay * LONG_STAY_DISCOUNT else 0.0
        if (longStay != 0.0) lines += QuoteLine(LineKind.LONG_STAY, longStay, percent = 10)

        val promo = if (promoPercent > 0) -(stay + extrasTotal + longStay) * promoPercent / 100.0 else 0.0
        if (promo != 0.0) lines += QuoteLine(LineKind.PROMO, promo, percent = promoPercent)

        val net = stay + extrasTotal + longStay + promo
        val tax = net * TAX_RATE
        lines += QuoteLine(LineKind.TAX, tax, percent = 10)
        return Quote(nights, lines, net + tax)
    }
}
