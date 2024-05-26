import 'package:flutter/material.dart';
import 'package:sky_sight/screens/locationError.dart';
import 'package:geolocator/geolocator.dart';
//import 'package:phosphor_flutter/phosphor_flutter.dart';
import 'package:provider/provider.dart';

import '../provider/weatherProvider.dart';
//import '../theme/colors.dart';
//import '../theme/textStyle.dart';
import '../widgets/WeatherInfoHeader.dart';
import '../widgets/mainWeatherDetail.dart';
import '../widgets/mainWeatherInfo.dart';
import '../widgets/fiveDayForecast.dart';
import '../widgets/twentyFourHourForecast.dart';

import 'requestError.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  void initState() {
    super.initState();
    requestWeather();
  }

  Future<void> requestWeather() async {
    await Provider.of<WeatherProvider>(context, listen: false)
        .getWeatherData(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Image.asset(
              'assets/images/icon.png',
              height: 28.0,
              width: 28.0,
            ),
            SizedBox(width: 8.0),
            Text("Sky Sight"),
            Spacer(),
          ],
        ),
        centerTitle: true,
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            color: const Color.fromARGB(255, 65, 221, 174),
            onPressed: requestWeather,
          ),
        ],
      ),
      body: Consumer<WeatherProvider>(
        builder: (context, weatherProv, _) {
          if (!weatherProv.isLoading && !weatherProv.isLocationserviceEnabled)
            return LocationServiceErrorDisplay();

          if (!weatherProv.isLoading &&
              weatherProv.locationPermission != LocationPermission.always &&
              weatherProv.locationPermission != LocationPermission.whileInUse) {
            return LocationPermissionErrorDisplay();
          }

          if (weatherProv.isRequestError) return RequestErrorDisplay();

          //if (weatherProv.isSearchError) return SearchErrorDisplay(fsc: null);

          return ListView(
            physics: BouncingScrollPhysics(),
            padding: const EdgeInsets.all(12.0).copyWith(
              top: kToolbarHeight +
                  MediaQuery.viewPaddingOf(context).top +
                  2.0,
            ),
            children: [
              WeatherInfoHeader(),
              const SizedBox(height: 16.0),
              MainWeatherInfo(),
              const SizedBox(height: 16.0),
              MainWeatherDetail(),
              const SizedBox(height: 24.0),
              TwentyFourHourForecast(),
              const SizedBox(height: 18.0),
              FiveDayForecast(),
            ],
          );
        },
      ),
    );
  }
}
