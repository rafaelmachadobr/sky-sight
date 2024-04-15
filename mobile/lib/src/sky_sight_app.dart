import 'package:asyncstate/asyncstate.dart';
import 'package:mobile/src/features/home/home_page.dart';
import 'package:flutter/material.dart';

class SkySightApp extends StatelessWidget {
  const SkySightApp({super.key});

  @override
  Widget build(BuildContext context) {
    return AsyncStateBuilder(
      builder: (asyncNavigatorObserver) {
        return MaterialApp(
          title: 'Sky Sight',
          navigatorObservers: [asyncNavigatorObserver],
          routes: {'/': (_) => const HomePage()},
        );
      },
    );
  }
}
