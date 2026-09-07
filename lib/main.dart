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
      title: 'Criador de Vídeo Automático',
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
  String? videoUrl;
  VideoPlayerController? _videoController;
  String statusMensagem = '';

  Future<void> gerarVideo() async {
    if (promptController.text.trim().isEmpty) return;

    setState(() {
      isLoading = true;
      videoUrl = null;
      statusMensagem = 'Conectando ao servidor...';
    });

    // Descarta o controller antigo se existir
    _videoController?.dispose();
    _videoController = null;

    try {
      // Configurado com 60 segundos para dar tempo do Render inicializar
      final response = await http.post(
        Uri.parse('https://geradorvideoq.onrender.com/gerar-video'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'prompt': promptController.text.trim()}),
      ).timeout(const Duration(seconds: 60));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final url = data['video_url'];

        if (url != null && url.isNotEmpty) {
          _inicializarPlayer(url);
        } else {
          _mostrarErro('Nenhum vídeo retornado.');
        }
      } else {
        _mostrarErro('Erro no servidor: ${response.statusCode}');
      }
    } catch (e) {
      _mostrarErro('O servidor demorou para responder. Tente novamente em alguns segundos.');
    }
  }

  void _inicializarPlayer(String url) {
    setState(() {
      statusMensagem = 'Carregando vídeo...';
    });

    _videoController = VideoPlayerController.networkUrl(Uri.parse(url))
      ..initialize().then((_) {
        setState(() {
          videoUrl = url;
          isLoading = false;
        });
        _videoController?.setLooping(true);
        _videoController?.play();
      }).catchError((error) {
        _mostrarErro('Erro ao reproduzir a mídia.');
      });
  }

  void _mostrarErro(String mensagem) {
    setState(() {
      isLoading = false;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(mensagem)),
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
      body: Padding(
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
                hintText: 'Ex: disco voador, galáxia, tecnologia...',
              ),
              maxLines: 3,
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
            if (isLoading) Text(statusMensagem),
            if (videoUrl != null && _videoController != null && _videoController!.value.isInitialized)
              Expanded(
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
