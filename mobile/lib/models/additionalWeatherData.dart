// ignore_for_file: public_member_api_docs, sort_constructors_first
class AdditionalWeatherData {
  final String precipitation;
  final int clouds;

  AdditionalWeatherData({
    required this.precipitation,
    required this.clouds,
  });

    factory AdditionalWeatherData.fromJson(Map<String, dynamic> json) {
    final List list = json['list'];
    double totalPrecipitation = 0.0;
    double totalClouds = 0;
    int count = list.length;

    for (var item in list) {
      totalPrecipitation += (item['pop'] ?? 0) * 100;
      if (item['clouds'] != null && item['clouds']['all'] != null) {
        totalClouds += item['clouds']['all'];
      }
    }

    final avgPrecipitation = (totalPrecipitation / count).toStringAsFixed(0);
    final avgClouds = (totalClouds / count).round();

    return AdditionalWeatherData(
      precipitation: avgPrecipitation,
      clouds: avgClouds,
    );
  }

  // AdditionalWeatherData.fromJson(Map<String, dynamic> json) {
  //   // Inicialize as propriedades com os dados do JSON
  // }

  // factory AdditionalWeatherData.fromJson(Map<String, dynamic> json) {
  //   final precipData = json['daily'][0]['pop'];
  //   final precip = (precipData * 100).toStringAsFixed(0);
  //   return AdditionalWeatherData(
  //     precipitation: precip,
  //     uvi: (json['daily'][0]['uvi']).toDouble(),
  //     clouds: json['daily'][0]['clouds'] ?? 0,
  //   );
  // }
}
