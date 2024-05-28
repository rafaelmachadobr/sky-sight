import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:provider/provider.dart';

import './provider/weatherProvider.dart';
import 'screens/homeScreen.dart';
import 'Screens/fiveDayForecastDetailScreen.dart';
//import 'package:intl/intl.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import '../models/dailyWeather.dart';

final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin = FlutterLocalNotificationsPlugin();

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initializeDateFormatting('pt_BR', null);
  await dotenv.load(fileName: ".env");

  WeatherProvider _weatherProvider = WeatherProvider();

  String alertDescription = _weatherProvider.dailyWeather.isNotEmpty 
    ? _weatherProvider.dailyWeather[0].alert 
    : 'Chuva forte prevista! Precipitação superior a 70%.';

  // Inicialize as configurações de notificações
  var initializationSettingsAndroid = AndroidInitializationSettings('@mipmap/ic_launcher');
  var initializationSettings = InitializationSettings(
      android: initializationSettingsAndroid);

  await flutterLocalNotificationsPlugin.initialize(initializationSettings);

  scheduleHourlyNotification(alertDescription);

  runApp(
    ChangeNotifierProvider.value( // Use ChangeNotifierProvider.value para passar uma instância existente
      value: _weatherProvider,
      child: MyApp(),
    ),
  );
}

void scheduleHourlyNotification(String alertDescription) async {

  var androidDetails = AndroidNotificationDetails(
    'channelId', // Identificador único do canal
    'channelName', // Nome do canal
    channelDescription: 'Este canal é usado para notificações periódicas.', // Descrição do canal
    importance: Importance.max,
    priority: Priority.high,
  );
  var generalNotificationDetails = NotificationDetails(
      android: androidDetails);

  await flutterLocalNotificationsPlugin.periodicallyShow(
    0,
    'ALERTA DO TEMPO',
    alertDescription,
    RepeatInterval.everyMinute,
    generalNotificationDetails,
    androidAllowWhileIdle: true,
  );

   print('Notificação agendada');
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => WeatherProvider(),
      child: MaterialApp(
        title: 'Sky Sight',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          appBarTheme: AppBarTheme(
            backgroundColor: Colors.white,
            iconTheme: IconThemeData(color: Colors.blue),
            elevation: 0,
          ),
          scaffoldBackgroundColor: Colors.white,
          primaryColor: Colors.blue,
          visualDensity: VisualDensity.adaptivePlatformDensity,
          colorScheme:
              ColorScheme.fromSwatch().copyWith(secondary: Colors.white),
        ),
        home: HomeScreen(),
        // routes: {
        //   WeeklyScreen.routeName: (ctx) => WeeklyScreen(),
        // },
        onGenerateRoute: (settings) {
          final arguments = settings.arguments;
          if (settings.name == FiveDayForecastDetail.routeName) {
            return PageRouteBuilder(
              settings: settings,
              pageBuilder: (_, __, ___) => FiveDayForecastDetail(
                initialIndex: arguments == null ? 0 : arguments as int,
              ),
              transitionsBuilder: (ctx, a, b, c) => CupertinoPageTransition(
                primaryRouteAnimation: a,
                secondaryRouteAnimation: b,
                linearTransition: false,
                child: c,
              ),
            );
          }
          //Unknown route
          return MaterialPageRoute(builder: (_) => HomeScreen());
        },
      ),
    );
  }
}
