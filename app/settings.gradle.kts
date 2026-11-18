rootProject.name = "LumbreHotel"
enableFeaturePreview("TYPESAFE_PROJECT_ACCESSORS")

pluginManagement {
    repositories {
        google {
            mavenContent {
                includeGroupAndSubgroups("androidx")
                includeGroupAndSubgroups("com.android")
                includeGroupAndSubgroups("com.google")
            }
        }
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositories {
        google {
            mavenContent {
                includeGroupAndSubgroups("androidx")
                includeGroupAndSubgroups("com.android")
                includeGroupAndSubgroups("com.google")
            }
        }
        mavenCentral()
    }
}

// shared     → todo el código común (lógica + interfaz Compose) para Android, iOS y web
// androidApp → punto de entrada Android (se abre y ejecuta desde Android Studio)
// webApp     → punto de entrada web (Kotlin/Wasm en el navegador)
// iosApp     → proyecto Xcode que incrusta el framework "Shared" (requiere macOS)
include(":shared")
include(":androidApp")
include(":webApp")
