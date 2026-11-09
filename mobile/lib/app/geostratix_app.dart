import 'package:flutter/material.dart';
import '../features/classification/presentation/classification_home_page.dart';

class GeoStratixApp extends StatelessWidget {
  const GeoStratixApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'GeoStratix',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.blueGrey),
      home: const ClassificationHomePage(),
    );
  }
}
