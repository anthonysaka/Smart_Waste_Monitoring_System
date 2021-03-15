import 'dart:convert';

import 'package:http/http.dart' as http;

class ApiProvider {
  Future<dynamic> getAllBins() async {
    final response = await http
        .get("http://10.0.2.2:5000/gomibako/internalapi/1.0/dustbin/2");

    if (response.statusCode == 200) {
      String body = utf8.decode(response.bodyBytes);
      final jsonData = jsonDecode(body);
      return jsonData;
    } else {
      throw Exception("Error API [getAllBins]");
    }
  }
}
