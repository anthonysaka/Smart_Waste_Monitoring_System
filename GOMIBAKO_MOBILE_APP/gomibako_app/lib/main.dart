import 'package:flutter/material.dart';
import 'package:gomibako_app/utils/config.helper.dart';
import 'package:gomibako_app/utils/location.helper.dart';
import 'package:mapbox_gl/mapbox_gl.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Gomibako Citizens',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: HomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: FutureBuilder(
        future: loadConfigFile(),
        builder: (
          BuildContext buildContext,
          AsyncSnapshot<Map<String, dynamic>> snapshot,
        ) {
          if (snapshot.hasData) {
            return MapboxMap(
              accessToken: snapshot.data['mapbox_api_token'],
              initialCameraPosition: CameraPosition(
                target: LatLng(20.20, 20.20),
              ),
              onMapCreated: (MapboxMapController controler) async {
                final location = await acquireCurrentLocation();
                final animateCameraResult = await controler.animateCamera(
                  CameraUpdate.newCameraPosition(
                    CameraPosition(
                      zoom: 15.0,
                      target: location,
                    ),
                  ),
                );

                if (animateCameraResult) {
                  controler.addCircle(CircleOptions(
                    circleRadius: 8.0,
                    circleColor: '#1696E0',
                    geometry: location,
                  ));
                }
              },
            );
          } else {
            return Center(
              child: CircularProgressIndicator(),
            );
          }
        },
      ),
      bottomNavigationBar: BottomNavigationBar(
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.add_comment),
            label: 'Reporte',
          ),
        ],
      ),
    );
  }
}
