package com.lumbre.hotel.ui.components

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.AcUnit
import androidx.compose.material.icons.rounded.Balcony
import androidx.compose.material.icons.rounded.Bathtub
import androidx.compose.material.icons.rounded.Coffee
import androidx.compose.material.icons.rounded.Deck
import androidx.compose.material.icons.rounded.KingBed
import androidx.compose.material.icons.rounded.Kitchen
import androidx.compose.material.icons.rounded.Pool
import androidx.compose.material.icons.rounded.Tv
import androidx.compose.material.icons.rounded.Water
import androidx.compose.material.icons.rounded.Weekend
import androidx.compose.material.icons.rounded.Wifi
import androidx.compose.ui.graphics.vector.ImageVector
import com.lumbre.hotel.data.Extra
import com.lumbre.hotel.data.ExtraUnit
import com.lumbre.hotel.data.ReservationStatus
import com.lumbre.hotel.data.RoomId
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.resources.Res
import com.lumbre.hotel.resources.day_morning
import com.lumbre.hotel.resources.dest_cove
import com.lumbre.hotel.resources.dest_sail
import com.lumbre.hotel.resources.dest_town
import com.lumbre.hotel.resources.dest_village
import com.lumbre.hotel.resources.exp_desk
import com.lumbre.hotel.resources.exp_food
import com.lumbre.hotel.resources.exp_pool
import com.lumbre.hotel.resources.exp_spa
import com.lumbre.hotel.resources.exp_trips
import com.lumbre.hotel.resources.exp_wifi
import com.lumbre.hotel.resources.room_deluxe
import com.lumbre.hotel.resources.room_penthouse
import com.lumbre.hotel.resources.room_standard
import org.jetbrains.compose.resources.DrawableResource

/** Contenido editorial fijo (fotos, textos y comodidades) asociado a cada habitación. */
data class RoomInfo(
    val id: RoomId,
    val name: K,
    val description: K,
    val image: DrawableResource,
    val sizeM2: Int,
    val rating: String,
    val reviews: Int,
    val amenities: List<Pair<ImageVector, K>>,
    val popular: Boolean = false,
)

object Catalog {
    val rooms = listOf(
        RoomInfo(
            RoomId.STANDARD, K.ROOM_STANDARD, K.ROOM_STANDARD_D, Res.drawable.room_standard, 24, "4,8", 412,
            listOf(Icons.Rounded.Deck to K.AM_GARDEN, Icons.Rounded.Wifi to K.AM_WIFI, Icons.Rounded.AcUnit to K.AM_AC,
                Icons.Rounded.Tv to K.AM_TV, Icons.Rounded.Coffee to K.AM_COFFEE),
        ),
        RoomInfo(
            RoomId.DELUXE, K.ROOM_DELUXE, K.ROOM_DELUXE_D, Res.drawable.room_deluxe, 42, "4,9", 638,
            listOf(Icons.Rounded.Water to K.AM_SEA, Icons.Rounded.Balcony to K.AM_BALCONY, Icons.Rounded.Bathtub to K.AM_BATH,
                Icons.Rounded.Weekend to K.AM_LOUNGE, Icons.Rounded.KingBed to K.AM_KING, Icons.Rounded.Wifi to K.AM_WIFI,
                Icons.Rounded.Kitchen to K.AM_MINIBAR),
            popular = true,
        ),
        RoomInfo(
            RoomId.PENTHOUSE, K.ROOM_PENTHOUSE, K.ROOM_PENTHOUSE_D, Res.drawable.room_penthouse, 95, "5,0", 121,
            listOf(Icons.Rounded.Pool to K.AM_POOL, Icons.Rounded.Water to K.AM_SEA, Icons.Rounded.KingBed to K.AM_KING,
                Icons.Rounded.Weekend to K.AM_LOUNGE, Icons.Rounded.Bathtub to K.AM_BATH, Icons.Rounded.Wifi to K.AM_WIFI,
                Icons.Rounded.AcUnit to K.AM_AC, Icons.Rounded.Kitchen to K.AM_MINIBAR),
        ),
    )

    fun room(id: RoomId): RoomInfo = rooms.first { it.id == id }

    data class Tile(val title: K, val sub: K, val image: DrawableResource, val extra: Extra? = null)

    val experiences = listOf(
        Tile(K.EXP_SPA, K.EXP_SPA_D, Res.drawable.exp_spa, Extra.SPA),
        Tile(K.EXP_FOOD, K.EXP_FOOD_D, Res.drawable.exp_food, Extra.BREAKFAST),
        Tile(K.EXP_POOL, K.EXP_POOL_D, Res.drawable.exp_pool),
        Tile(K.EXP_DESK, K.EXP_DESK_D, Res.drawable.exp_desk, Extra.TRANSFER),
        Tile(K.EXP_WIFI, K.EXP_WIFI_D, Res.drawable.exp_wifi),
        Tile(K.EXP_TRIPS, K.EXP_TRIPS_D, Res.drawable.exp_trips),
    )

    val destinations = listOf(
        Tile(K.DEST_1, K.DEST_1_D, Res.drawable.dest_cove),
        Tile(K.DEST_2, K.DEST_2_D, Res.drawable.dest_village),
        Tile(K.DEST_3, K.DEST_3_D, Res.drawable.dest_town),
        Tile(K.DEST_4, K.DEST_4_D, Res.drawable.dest_sail),
    )

    val reviews = listOf(K.REV_1 to "Marta · Madrid", K.REV_2 to "James · London", K.REV_3 to "Camille · Lyon")

    val heroFallback = Res.drawable.day_morning

    fun extraName(e: Extra): K = when (e) {
        Extra.BREAKFAST -> K.X_BREAKFAST; Extra.SPA -> K.X_SPA; Extra.TRANSFER -> K.X_TRANSFER
        Extra.PARKING -> K.X_PARKING; Extra.LATE_CHECKOUT -> K.X_LATE_CHECKOUT
    }

    fun extraUnit(e: Extra): K = when (e.unit) {
        ExtraUnit.PER_PERSON_NIGHT -> K.U_PER_PERSON_NIGHT; ExtraUnit.PER_ADULT -> K.U_PER_ADULT
        ExtraUnit.PER_STAY -> K.U_PER_STAY; ExtraUnit.PER_NIGHT -> K.U_PER_NIGHT
    }

    fun status(s: ReservationStatus): K = when (s) {
        ReservationStatus.CONFIRMED -> K.ST_CONFIRMED
        ReservationStatus.CHECKED_IN -> K.ST_CHECKED_IN
        ReservationStatus.CANCELLED -> K.ST_CANCELLED
    }
}
