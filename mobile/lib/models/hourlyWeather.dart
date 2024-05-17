// ignore_for_file: public_member_api_docs, sort_constructors_first
class HourlyWeather {
  final double temp;
  final String weatherCategory;
  final String? condition;
  final DateTime date;

  HourlyWeather({
    required this.temp,
    required this.weatherCategory,
    this.condition,
    required this.date,
  });

  // HourlyWeather.fromJson(Map<String, dynamic> json) {
  //   // Inicialize as propriedades com os dados do JSON
  // }

  static HourlyWeather fromJson(dynamic json) {
    return HourlyWeather(
      temp: (json['main']['temp']).toDouble(),
      weatherCategory: json['weather'][0]['main'],
      condition: json['weather'][0]['description'],
      date: DateTime.parse(json['dt_txt']),
    );
  }
}
