package com.lumbre.hotel.domain

import com.lumbre.hotel.data.Currency
import com.lumbre.hotel.data.Lang
import kotlinx.datetime.LocalDate
import kotlinx.datetime.number
import kotlin.math.abs
import kotlin.math.roundToLong

/** Formato propio (sin depender de la plataforma), igual en Android, iOS y web. */
object Format {
    private fun group(n: Long, sep: Char): String {
        val s = abs(n).toString()
        val sb = StringBuilder()
        s.forEachIndexed { i, c ->
            if (i > 0 && (s.length - i) % 3 == 0) sb.append(sep)
            sb.append(c)
        }
        return (if (n < 0) "-" else "") + sb
    }

    fun money(eur: Double, currency: Currency, lang: Lang): String {
        val v = (eur * currency.rate).roundToLong()
        val sep = if (lang == Lang.EN) ',' else '.'
        val n = group(v, sep)
        return when {
            currency == Currency.EUR && lang != Lang.EN -> "$n €"
            currency == Currency.EUR -> "€$n"
            currency == Currency.BRL -> "R$ $n"
            else -> "${currency.symbol}$n"
        }
    }

    private val months = mapOf(
        Lang.ES to listOf("ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sept", "oct", "nov", "dic"),
        Lang.EN to listOf("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"),
        Lang.PT to listOf("jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"),
        Lang.FR to listOf("janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."),
    )

    fun shortDate(date: LocalDate, lang: Lang): String {
        val m = months.getValue(lang)[date.month.number - 1]
        return if (lang == Lang.EN) "$m ${date.day}" else "${date.day} $m"
    }

    fun range(from: LocalDate, to: LocalDate, lang: Lang): String =
        "${shortDate(from, lang)} – ${shortDate(to, lang)}"
}
