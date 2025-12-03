import 'package:flutter/material.dart';

// Importing all screens
import 'screens/home_screen.dart';
import 'screens/logs_screen.dart';
import 'screens/control_screen.dart';
import 'screens/settings_screen.dart';

// Importing the custom app theme
import 'theme/app_theme.dart';

void main() {
  runApp(const PillApp()); // ✅ Consistent class name (PillApp, not PillAPP)
}

// Main App Widget — Stateful because the bottom nav bar changes screens
class PillApp extends StatefulWidget {
  const PillApp({super.key});

  @override
  State<PillApp> createState() => _PillAppState();
}

class _PillAppState extends State<PillApp> {
  // Tracks the selected navigation index
  int _selectedIndex = 0;

  // List of screens for the bottom navigation
  final List<Widget> _screens = const [
    HomeScreen(),
    ControlScreen(),
    LogsScreen(),
    SettingsScreen(), // ✅ Fixed typo: SettingScreen → SettingsScreen
  ];

  // Handles navigation when a tab is tapped
  void _onItemTapped(int index) {
    setState(() => _selectedIndex = index);
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp( // ✅ Changed from `Material` to `MaterialApp`
      title: 'Team Sigma Control Center',
      debugShowCheckedModeBanner: false, // ✅ Fixed property name
      theme: AppTheme.darkTheme,
      home: Scaffold(
        backgroundColor: const Color(0xFF0B0E21),
        // Smooth transition when switching between screens
        body: AnimatedSwitcher(
          duration: const Duration(milliseconds: 400),
          child: _screens[_selectedIndex],
        ),
        bottomNavigationBar: BottomNavigationBar(
          backgroundColor: const Color(0xFF14172B),
          selectedItemColor: Colors.cyanAccent,
          unselectedItemColor: Colors.white70,
          currentIndex: _selectedIndex,
          type: BottomNavigationBarType.fixed,
          onTap: _onItemTapped,
          items: const [
            BottomNavigationBarItem(
              icon: Icon(Icons.home),
              label: 'Home',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.sports_esports),
              label: 'Control',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.list_alt),
              label: 'Logs',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.settings),
              label: 'Settings',
            ),
          ],
        ),
      ),
    );
  }
}
