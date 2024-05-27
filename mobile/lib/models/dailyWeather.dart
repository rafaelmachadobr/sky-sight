// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'package:flutter/cupertino.dart';

class DailyWeather with ChangeNotifier {
  final double temp;
  final double tempMin;
  final double tempMax;
  final double tempMorning;
  final double tempDay;
  final double tempEvening;
  final double tempNight;
  final String weatherCategory;
  final String condition;
  final DateTime date;
  final String precipitation;
  final int clouds;
  final int humidity;
  final String tip;
  final String alert;

  DailyWeather({
    required this.temp,
    required this.tempMin,
    required this.tempMax,
    required this.tempMorning,
    required this.tempDay,
    required this.tempEvening,
    required this.tempNight,
    required this.weatherCategory,
    required this.condition,
    required this.date,
    required this.precipitation,
    required this.clouds,
    required this.humidity,
    required this.tip,
    required this.alert
  });

  // DailyWeather.fromDailyJson(Map<String, dynamic> json) {
  //   // Inicialize as propriedades com os dados do JSON
  // }

  static DailyWeather fromDailyJson(List<dynamic> json) {
    // Agregar dados a partir da lista de previsões horárias para um dia
    double tempSum = 0;
    double tempMin = double.infinity;
    double tempMax = -double.infinity;
    double tempMorning = 0;
    double tempDay = 0;
    double tempEvening = 0;
    double tempNight = 0;
    int morningCount = 0;
    int dayCount = 0;
    int eveningCount = 0;
    int nightCount = 0;
    double precipitationSum = 0;
    double cloudsSum = 0;
    double humiditySum = 0;
    int count = json.length;
    String weatherCategory = json[0]['weather'][0]['main'];
    String condition = json[0]['weather'][0]['description'];
    DateTime date = DateTime.parse(json[0]['dt_txt']);
    String tip = json[0]['tip'];
    String alert = json[0]['alert']['title'];


    for (var item in json) {
      double temp = item['main']['temp'].toDouble();
      tempSum += temp;
      tempMin = temp < tempMin ? temp : tempMin;
      tempMax = temp > tempMax ? temp : tempMax;

      DateTime itemDate = DateTime.parse(item['dt_txt']);
      int hour = itemDate.hour;

      if (hour >= 6 && hour < 12) {
        tempMorning += temp;
        morningCount++;
      } else if (hour >= 12 && hour < 18) {
        tempDay += temp;
        dayCount++;
      } else if (hour >= 18 && hour < 24) {
        tempEvening += temp;
        eveningCount++;
      } else {
        tempNight += temp;
        nightCount++;
      }

      precipitationSum += (item['pop'] ?? 0) * 100;
      cloudsSum += item['clouds']['all'] ?? 0;
      humiditySum += item['main']['humidity'] ?? 0;
    }

    return DailyWeather(
      temp: tempSum / count,
      tempMin: tempMin,
      tempMax: tempMax,
      tempMorning: morningCount > 0 ? tempMorning / morningCount : 0,
      tempDay: dayCount > 0 ? tempDay / dayCount : 0,
      tempEvening: eveningCount > 0 ? tempEvening / eveningCount : 0,
      tempNight: nightCount > 0 ? tempNight / nightCount : 0,
      weatherCategory: weatherCategory,
      condition: condition,
      date: date,
      precipitation: (precipitationSum / count).toStringAsFixed(0),
      clouds: (cloudsSum / count).round(),
      humidity: (humiditySum / count).round(),
      tip : tip,
      alert : alert,
    );
  }

  // static DailyWeather fromDailyJson(dynamic json) {
  //   return DailyWeather(
  //     temp: (json['temp']['day']).toDouble(),
  //     tempMin: (json['temp']['min']).toDouble(),
  //     tempMax: (json['temp']['max']).toDouble(),
  //     tempMorning: (json['feels_like']['morn']).toDouble(),
  //     tempDay: (json['feels_like']['day']).toDouble(),
  //     tempEvening: (json['feels_like']['eve']).toDouble(),
  //     tempNight: (json['feels_like']['night']).toDouble(),
  //     weatherCategory: json['weather'][0]['main'],
  //     condition: json['weather'][0]['description'],
  //     date: DateTime.fromMillisecondsSinceEpoch(json['dt'] * 1000, isUtc: true),
  //     precipitation: ((json['pop']).toDouble() * 100).toStringAsFixed(0),
  //     clouds: json['clouds'],
  //     humidity: json['humidity'],
  //   );
  // }
}
