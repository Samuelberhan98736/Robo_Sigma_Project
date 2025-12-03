import 'package:flutter/material.dart';

class AppTheme {
  static final darkTheme = ThemeData(
    brightness: Brightness.dark,
    scaffoldBackgroundColor: const Color(0xFF0B0E21),
    fontFamily: 'Orbitron',
    textTheme: const TextTheme(
      bodyLarge: TextStyle(color: Colors.white, fontSize: 18),
      bodyMedium: TextStyle(color: Colors.white70, fontSize: 16),
      headlineSmall: TextStyle(
        color: Colors.cyanAccent,
        fontWeight: FontWeight.bold,
      ),
    ),
    appBarTheme: const AppBarTheme(
      backgroundColor: Color(0xFF0B0E21),
      elevation: 0,
    ),
  );
}
