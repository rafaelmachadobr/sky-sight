import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_weather/models/additionalWeatherData.dart';
import 'package:flutter_weather/models/geocode.dart';
import 'package:geolocator/geolocator.dart';
import 'package:http/http.dart' as http;
import 'package:latlong2/latlong.dart';

import '../models/dailyWeather.dart';
import '../models/hourlyWeather.dart';
import '../models/weather.dart';

class WeatherProvider with ChangeNotifier {
  String apiKey = dotenv.env['OPENWEATHERMAP_API_KEY']!;
  late Weather weather;
  late AdditionalWeatherData additionalWeatherData;
  LatLng? currentLocation;
  List<HourlyWeather> hourlyWeather = [];
  List<DailyWeather> dailyWeather = [];
  bool isLoading = false;
  bool isRequestError = false;
  bool isSearchError = false;
  bool isLocationserviceEnabled = false;
  LocationPermission? locationPermission;
  bool isCelsius = true;

  String get measurementUnit => isCelsius ? '°C' : '°F';

  Future<Position?> requestLocation(BuildContext context) async {
    isLocationserviceEnabled = await Geolocator.isLocationServiceEnabled();
    notifyListeners();

    if (!isLocationserviceEnabled) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Location service disabled')),
      );
      return Future.error('Location services are disabled.');
    }

    locationPermission = await Geolocator.checkPermission();
    if (locationPermission == LocationPermission.denied) {
      isLoading = false;
      notifyListeners();
      locationPermission = await Geolocator.requestPermission();
      if (locationPermission == LocationPermission.denied) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text('Permission denied'),
        ));
        return Future.error('Location permissions are denied');
      }
    }

    if (locationPermission == LocationPermission.deniedForever) {
      isLoading = false;
      notifyListeners();
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text(
          'Location permissions are permanently denied, Please enable manually from app settings',
        ),
      ));
      return Future.error('Location permissions are permanently denied');
    }

    return await Geolocator.getCurrentPosition();
  }

  Future<void> getWeatherData(
    BuildContext context, {
    bool notify = false,
  }) async {
    isLoading = true;
    isRequestError = false;
    isSearchError = false;
    if (notify) notifyListeners();

    Position? locData = await requestLocation(context);

    if (locData == null) {
      isLoading = false;
      notifyListeners();
      return;
    }

    try {
      currentLocation = LatLng(locData.latitude, locData.longitude);
      await getCurrentWeather(currentLocation!);
      await getDailyWeather(currentLocation!);
    } catch (e) {
      print(e);
      isRequestError = true;
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  Future<void> getCurrentWeather(LatLng location) async {
    Uri url = Uri.parse(
      'https://api.openweathermap.org/data/2.5/weather?lat=-23.587405&lon=-46.65773&units=metric&appid=$apiKey&lang=pt_br',
    );
    try {
      final response = await http.get(url);
      final extractedData = json.decode(response.body) as Map<String, dynamic>;
      weather = Weather.fromJson(extractedData);
      print('Fetched Weather for: ${weather.city}/${weather.countryCode}');
    } catch (error) {
      print(error);
      isLoading = false;
      this.isRequestError = true;
    }
  }

  Future<void> getDailyWeather(LatLng location) async {
    isLoading = true;
    notifyListeners();

    Uri dailyUrl = Uri.parse(
      'https://api.openweathermap.org/data/2.5/forecast?lat=-23.587405&lon=-46.65773&lang=pt_br&appid=$apiKey&units=metric',
    );
    try {
      final response = await http.get(dailyUrl);
      if(response.statusCode == 200){
      final dailyData = json.decode(response.body) as Map<String, dynamic>;
      additionalWeatherData = AdditionalWeatherData.fromJson(dailyData);
      //List dailyList = dailyData['daily'];
      List hourlyList = dailyData['list'];

        // Filtrando previsões para hoje em intervalos de 3 horas
      DateTime now = DateTime.now();
      DateTime endOfDay = DateTime(now.year, now.month, now.day, 23, 59, 59).add(Duration(days: 4));;
      hourlyWeather = hourlyList
          .map((item) => HourlyWeather.fromJson(item))
          .where((item) => item.date.isAfter(now) && item.date.isBefore(endOfDay))
          .toList();
      // Convertendo a lista de 3 em 3 horas para HourlyWeather
        // hourlyWeather = hourlyList
        //     .map((item) => HourlyWeather.fromJson(item))
        //     .toList()
        //     .take(24)
        //     .toList();

      // hourlyWeather = hourlyList
      //     .map((item) => HourlyWeather.fromJson(item))
      //     .toList()
      //     .take(24)
      //     .toList();

      // Agrupando por dias
        Map<String, List> groupedDailyData = {};
        hourlyList.forEach((item) {
          String date = item['dt_txt'].split(' ')[0];
          if (groupedDailyData[date] == null) {
            groupedDailyData[date] = [];
          }
          groupedDailyData[date]!.add(item);
        });

        dailyWeather = groupedDailyData.entries.map((entry) {
          // Aqui você pode definir como quer agregar os dados diários
          // Por exemplo, pegar a previsão do meio-dia ou a média dos dados do dia
          // No exemplo, pegaremos o primeiro item do dia
          return DailyWeather.fromDailyJson(entry.value);
        }).toList();


      // dailyWeather =
      //     dailyList.map((item) => DailyWeather.fromDailyJson(item)).toList();
      } else{
        throw Exception('Failed to load weather data');
      }

    } catch (error) {
      print(error);
      isLoading = false;
      this.isRequestError = true;
    }
  }

  Future<GeocodeData?> locationToLatLng(String location) async {
    try {
      Uri url = Uri.parse(
        'http://api.openweathermap.org/geo/1.0/direct?q=$location&limit=5&appid=$apiKey&lang=pt_br',
      );
      final http.Response response = await http.get(url);
      if (response.statusCode != 200) return null;
      return GeocodeData.fromJson(
        jsonDecode(response.body)[0] as Map<String, dynamic>,
      );
    } catch (e) {
      print(e);
      return null;
    }
  }

  Future<void> searchWeather(String location) async {
    isLoading = true;
    notifyListeners();
    isRequestError = false;
    print('search');
    try {
      GeocodeData? geocodeData;
      geocodeData = await locationToLatLng(location);
      if (geocodeData == null) throw Exception('Unable to Find Location');
      await getCurrentWeather(geocodeData.latLng);
      await getDailyWeather(geocodeData.latLng);
      // replace location name with data from geocode
      // because data from certain lat long might return local area name
      weather.city = geocodeData.name;
    } catch (e) {
      print(e);
      isSearchError = true;
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  void switchTempUnit() {
    isCelsius = !isCelsius;
    notifyListeners();
  }
}
