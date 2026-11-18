package com.lumbre.hotel.ui.navigation

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.AdminPanelSettings
import androidx.compose.material.icons.rounded.Home
import androidx.compose.material.icons.rounded.KingBed
import androidx.compose.material.icons.rounded.Luggage
import androidx.compose.material.icons.rounded.Person
import androidx.compose.ui.graphics.vector.ImageVector
import com.lumbre.hotel.i18n.K
import kotlinx.serialization.Serializable
import kotlin.reflect.KClass

@Serializable data object HomeRoute
@Serializable data object RoomsRoute
@Serializable data object TripsRoute
@Serializable data object ProfileRoute
@Serializable data object AdminRoute
@Serializable data class RoomDetailRoute(val room: String)
@Serializable data class BookingRoute(val room: String? = null, val checkIn: String? = null, val checkOut: String? = null, val guests: Int = 2)
@Serializable data class KeyRoute(val ref: String)

enum class Tab(val route: Any, val routeClass: KClass<*>, val label: K, val icon: ImageVector) {
    HOME(HomeRoute, HomeRoute::class, K.TAB_HOME, Icons.Rounded.Home),
    ROOMS(RoomsRoute, RoomsRoute::class, K.TAB_ROOMS, Icons.Rounded.KingBed),
    TRIPS(TripsRoute, TripsRoute::class, K.TAB_TRIPS, Icons.Rounded.Luggage),
    PROFILE(ProfileRoute, ProfileRoute::class, K.TAB_PROFILE, Icons.Rounded.Person),
    ADMIN(AdminRoute, AdminRoute::class, K.TAB_ADMIN, Icons.Rounded.AdminPanelSettings),
}
