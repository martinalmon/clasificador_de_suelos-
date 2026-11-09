import 'package:flutter/material.dart';

/// Pantalla inicial. Los formularios se agregarán después de verificar el motor.
class ClassificationHomePage extends StatelessWidget {
  const ClassificationHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('GeoStratix')),
      body: const Center(
        child: Padding(
          padding: EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.science_outlined, size: 56),
              SizedBox(height: 16),
              Text('Clasificación SUCS', style: TextStyle(fontSize: 24)),
              SizedBox(height: 8),
              Text(
                'Proyecto inicial. En la siguiente etapa agregaremos '
                'la captura y el motor de clasificación en Python.',
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
