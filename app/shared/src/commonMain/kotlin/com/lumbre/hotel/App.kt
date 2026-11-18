package com.lumbre.hotel

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.SharedTransitionLayout
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.scaleIn
import androidx.compose.animation.scaleOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationRail
import androidx.compose.material3.NavigationRailItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.SnackbarResult
import androidx.compose.material3.Text
import androidx.compose.material3.VerticalDivider
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavDestination.Companion.hasRoute
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.toRoute
import com.lumbre.hotel.data.AppGraph
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.i18n.LocalLang
import com.lumbre.hotel.i18n.regionName
import com.lumbre.hotel.i18n.t
import com.lumbre.hotel.i18n.tr
import com.lumbre.hotel.platform.Capabilities
import com.lumbre.hotel.ui.components.LocalCurrency
import com.lumbre.hotel.ui.components.LocalNavScope
import com.lumbre.hotel.ui.components.LocalSharedScope
import com.lumbre.hotel.ui.components.LocalSnackbar
import com.lumbre.hotel.ui.components.LocalWide
import com.lumbre.hotel.ui.components.Lumi
import com.lumbre.hotel.ui.components.Mood
import com.lumbre.hotel.ui.navigation.AdminRoute
import com.lumbre.hotel.ui.navigation.BookingRoute
import com.lumbre.hotel.ui.navigation.HomeRoute
import com.lumbre.hotel.ui.navigation.KeyRoute
import com.lumbre.hotel.ui.navigation.ProfileRoute
import com.lumbre.hotel.ui.navigation.RoomDetailRoute
import com.lumbre.hotel.ui.navigation.RoomsRoute
import com.lumbre.hotel.ui.navigation.Tab
import com.lumbre.hotel.ui.navigation.TripsRoute
import com.lumbre.hotel.ui.screens.AdminScreen
import com.lumbre.hotel.ui.screens.BookingScreen
import com.lumbre.hotel.ui.screens.HomeScreen
import com.lumbre.hotel.ui.screens.KeyScreen
import com.lumbre.hotel.ui.screens.PrefsSheet
import com.lumbre.hotel.ui.screens.ProfileScreen
import com.lumbre.hotel.ui.screens.RoomDetailScreen
import com.lumbre.hotel.ui.screens.RoomsScreen
import com.lumbre.hotel.ui.screens.TripsScreen
import com.lumbre.hotel.ui.theme.LumbreTheme

/** Punto de entrada común: lo llaman Android (MainActivity), iOS (MainViewController) y la web (main.kt). */
@Composable
fun App() {
    val repo = AppGraph.repo
    val prefs by repo.prefs.collectAsState()
    val snackbar = remember { SnackbarHostState() }
    var showPrefs by remember { mutableStateOf(false) }

    LumbreTheme(dark = isSystemInDarkTheme()) {
        CompositionLocalProvider(
            LocalLang provides prefs.lang,
            LocalCurrency provides prefs.currency,
            LocalSnackbar provides snackbar,
        ) {
            BoxWithConstraints(Modifier.fillMaxSize()) {
                val wide = maxWidth >= 840.dp
                CompositionLocalProvider(LocalWide provides wide) {
                    val nav = rememberNavController()
                    val entry by nav.currentBackStackEntryAsState()
                    val destination = entry?.destination
                    val tabs = Tab.entries.filter { it != Tab.ADMIN || (Capabilities.adminPanel && prefs.admin) }
                    val current = tabs.firstOrNull { destination?.hasRoute(it.routeClass) == true }

                    // Aviso de región la primera vez: idioma y moneda elegidos según desde dónde se accede.
                    LaunchedEffect(Unit) {
                        if (!prefs.regionNoticeShown) {
                            repo.markRegionNoticeShown()
                            val region = regionName(prefs.region, prefs.lang) ?: return@LaunchedEffect
                            val result = snackbar.showSnackbar(
                                tr(prefs.lang, K.REGION_NOTICE, region, prefs.currency.code),
                                actionLabel = tr(prefs.lang, K.CHANGE), withDismissAction = true,
                            )
                            if (result == SnackbarResult.ActionPerformed) showPrefs = true
                        }
                    }

                    Row(Modifier.fillMaxSize()) {
                        if (wide) {
                            NavigationRail(
                                containerColor = MaterialTheme.colorScheme.surfaceContainerLow,
                                header = {
                                    Lumi(Mood.Happy, trigger = Unit, modifier = Modifier.padding(top = 16.dp).size(52.dp))
                                    Text("Lumbre", style = MaterialTheme.typography.titleMedium)
                                    Spacer(Modifier.height(24.dp))
                                },
                            ) {
                                tabs.forEach { tab ->
                                    NavigationRailItem(
                                        selected = current == tab,
                                        onClick = { nav.goToTab(tab) },
                                        icon = { Icon(tab.icon, null) },
                                        label = { Text(t(tab.label)) },
                                    )
                                }
                            }
                            VerticalDivider(Modifier.fillMaxHeight(), color = MaterialTheme.colorScheme.outlineVariant)
                        }
                        Scaffold(
                            modifier = Modifier.weight(1f),
                            contentWindowInsets = WindowInsets(0, 0, 0, 0),
                            snackbarHost = { SnackbarHost(snackbar) },
                            bottomBar = {
                                AnimatedVisibility(
                                    visible = !wide && current != null,
                                    enter = slideInVertically { it } + fadeIn(),
                                    exit = slideOutVertically { it } + fadeOut(),
                                ) {
                                    NavigationBar(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest) {
                                        tabs.forEach { tab ->
                                            NavigationBarItem(
                                                selected = current == tab,
                                                onClick = { nav.goToTab(tab) },
                                                icon = { Icon(tab.icon, null) },
                                                label = { Text(t(tab.label), maxLines = 1, softWrap = false, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis, style = MaterialTheme.typography.labelSmall) },
                                            )
                                        }
                                    }
                                }
                            },
                        ) { padding ->
                            Box(Modifier.fillMaxSize().padding(padding)) {
                                AppNavHost(nav, onOpenPrefs = { showPrefs = true })
                            }
                        }
                    }
                    if (showPrefs) PrefsSheet(onDismiss = { showPrefs = false })
                }
            }
        }
    }
}

private fun NavHostController.goToTab(tab: Tab) {
    navigate(tab.route) {
        popUpTo(HomeRoute) { saveState = true }
        launchSingleTop = true
        restoreState = true
    }
}

@Composable
private fun AppNavHost(nav: NavHostController, onOpenPrefs: () -> Unit) {
    SharedTransitionLayout {
        CompositionLocalProvider(LocalSharedScope provides this) {
            NavHost(
                navController = nav,
                startDestination = HomeRoute,
                enterTransition = { fadeIn(tween(320)) + scaleIn(initialScale = 0.98f, animationSpec = tween(320)) },
                exitTransition = { fadeOut(tween(200)) },
                popEnterTransition = { fadeIn(tween(320)) },
                popExitTransition = { fadeOut(tween(200)) + scaleOut(targetScale = 0.98f, animationSpec = tween(200)) },
            ) {
                composable<HomeRoute> {
                    CompositionLocalProvider(LocalNavScope provides this) {
                        HomeScreen(
                            onRoom = { nav.navigate(RoomDetailRoute(it.name)) },
                            onBook = { nav.navigate(it) },
                            onSeeRooms = { nav.goToTab(Tab.ROOMS) },
                            onOpenPrefs = onOpenPrefs,
                        )
                    }
                }
                composable<RoomsRoute> {
                    CompositionLocalProvider(LocalNavScope provides this) {
                        RoomsScreen(onRoom = { nav.navigate(RoomDetailRoute(it.name)) })
                    }
                }
                composable<RoomDetailRoute>(
                    enterTransition = { fadeIn(tween(300)) },
                    popExitTransition = { fadeOut(tween(250)) },
                ) { backStack ->
                    val route = backStack.toRoute<RoomDetailRoute>()
                    CompositionLocalProvider(LocalNavScope provides this) {
                        RoomDetailScreen(
                            roomName = route.room,
                            onBack = { nav.popBackStack() },
                            onBook = { nav.navigate(BookingRoute(room = route.room)) },
                        )
                    }
                }
                composable<BookingRoute>(
                    enterTransition = { slideInHorizontally(tween(380)) { it / 3 } + fadeIn(tween(300)) },
                    popExitTransition = { slideOutHorizontally(tween(300)) { it / 3 } + fadeOut(tween(250)) },
                ) { backStack ->
                    CompositionLocalProvider(LocalNavScope provides this) {
                        BookingScreen(
                            route = backStack.toRoute<BookingRoute>(),
                            onClose = { nav.popBackStack() },
                            onTrips = {
                                nav.navigate(TripsRoute) { popUpTo(HomeRoute); launchSingleTop = true }
                            },
                            onHome = { nav.navigate(HomeRoute) { popUpTo(HomeRoute) { inclusive = true } } },
                        )
                    }
                }
                composable<TripsRoute> {
                    CompositionLocalProvider(LocalNavScope provides this) {
                        TripsScreen(
                            onBook = { nav.navigate(BookingRoute()) },
                            onKey = { nav.navigate(KeyRoute(it)) },
                        )
                    }
                }
                composable<KeyRoute>(
                    enterTransition = { slideInVertically(tween(420)) { it } + fadeIn() },
                    popExitTransition = { slideOutVertically(tween(320)) { it } + fadeOut() },
                ) { backStack ->
                    KeyScreen(ref = backStack.toRoute<KeyRoute>().ref, onClose = { nav.popBackStack() })
                }
                composable<ProfileRoute> {
                    ProfileScreen(onOpenAdmin = { nav.goToTab(Tab.ADMIN) })
                }
                composable<AdminRoute> {
                    AdminScreen(onGoProfile = { nav.goToTab(Tab.PROFILE) })
                }
            }
        }
    }
}
