import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:video_player/video_player.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Criador de Vídeo',
      theme: ThemeData.dark(),
      home: const VideoHomeScreen(),
    );
  }
}

class VideoHomeScreen extends StatefulWidget {
  const VideoHomeScreen({super.key});

  @override
  State<VideoHomeScreen> createState() => _VideoHomeScreenState();
}

class _VideoHomeScreenState extends State<VideoHomeScreen> {
  final TextEditingController promptController = TextEditingController();
  bool isLoading = false;
  VideoPlayerController? _videoController;
  String statusMensagem = '';

  Future<void> gerarVideo() async {
    final texto = promptController.text.trim();
    if (texto.isEmpty) return;

    FocusScope.of(context).unfocus(); // Fecha o teclado

    setState(() {
      isLoading = true;
      statusMensagem = 'Conectando ao servidor...';
    });

    _videoController?.dispose();
    _videoController = null;

    try {
      final response = await http.post(
        Uri.parse('https://geradorvideoq.onrender.com/gerar-video'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'prompt': texto}),
      ).timeout(const Duration(seconds: 45));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final String? url = data['video_url'];

        if (url != null && url.isNotEmpty) {
          setState(() {
            statusMensagem = 'Baixando e preparando vídeo...';
          });
          await _carregarVideoComSuporte(url);
        } else {
          _erro('Servidor não retornou o link do vídeo.');
        }
      } else {
        _erro('Erro no servidor (${response.statusCode}).');
      }
    } catch (e) {
      _erro('O servidor demorou a responder. Tente novamente.');
    }
  }

  Future<void> _carregarVideoComSuporte(String url) async {
    try {
      final controller = VideoPlayerController.networkUrl(
        Uri.parse(url),
        videoPlayerOptions: VideoPlayerOptions(mixWithOthers: true),
      );

      await controller.initialize();
      controller.setLooping(true);
      await controller.play();

      setState(() {
        _videoController = controller;
        isLoading = false;
      });
    } catch (e) {
      _erro('O formato do vídeo enviado não rodou no celular.');
    }
  }

  void _erro(String msg) {
    setState(() {
      isLoading = false;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(msg), backgroundColor: Colors.redAccent),
    );
  }

  @override
  void dispose() {
    _videoController?.dispose();
    promptController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Criador de Vídeo Automático'),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            const Text(
              'O que você deseja criar hoje?',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: promptController,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Ex: disco voador, galáxia...',
              ),
              maxLines: 2,
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              height: 48,
              child: ElevatedButton(
                onPressed: isLoading ? null : gerarVideo,
                child: isLoading
                    ? const CircularProgressIndicator(color: Colors.white)
                    : const Text('GERAR VÍDEO'),
              ),
            ),
            const SizedBox(height: 20),
            if (isLoading)
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text(statusMensagem, style: const TextStyle(color: Colors.amber)),
              ),
            if (_videoController != null && _videoController!.value.isInitialized)
              Container(
                height: 350,
                width: double.infinity,
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.purpleAccent, width: 2),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: AspectRatio(
                  aspectRatio: _videoController!.value.aspectRatio,
                  child: VideoPlayer(_videoController!),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
