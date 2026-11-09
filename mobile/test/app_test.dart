import 'package:flutter_test/flutter_test.dart';
import 'package:geostratix_mobile/app/geostratix_app.dart';

void main() {
  testWidgets('muestra el nombre y módulo inicial', (tester) async {
    await tester.pumpWidget(const GeoStratixApp());
    expect(find.text('GeoStratix'), findsOneWidget);
    expect(find.text('Clasificación SUCS'), findsOneWidget);
  });
}
