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
      title: 'Criador de Vídeo',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF121212),
        primaryColor: Colors.deepPurple,
      ),
      home: const VideoGeneratorScreen(),
    );
  }
}

class VideoGeneratorScreen extends StatefulWidget {
  const VideoGeneratorScreen({super.key});

  @override
  State<VideoGeneratorScreen> createState() => _VideoGeneratorScreenState();
}

class _VideoGeneratorScreenState extends State<VideoGeneratorScreen> {
  final TextEditingController _controller = TextEditingController();
  bool _isLoading = false;
  String? _errorMessage;
  VideoPlayerController? _videoController;

  Future<void> _generateVideo() async {
    final prompt = _controller.text.trim();
    if (prompt.isEmpty) return;

    FocusScope.of(context).unfocus(); // Fecha o teclado mobile ao clicar

    setState(() {
      _isLoading = true;
      _errorMessage = null;
      _videoController?.dispose();
      _videoController = null;
    });

    try {
      // 1. Tenta a chamada no backend
      final response = await http
          .post(
            Uri.parse('https://geradorvideoq.onrender.com/gerar-video'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({'prompt': prompt}),
          )
          .timeout(const Duration(seconds: 12)); // Define tempo limite para não travar a tela

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final videoUrl = data['video_url'];

        if (videoUrl != null && videoUrl.toString().isNotEmpty) {
          _initializeVideoPlayer(videoUrl);
        } else {
          _useDirectIaFallback(prompt);
        }
      } else {
        _useDirectIaFallback(prompt);
      }
    } catch (e) {
      // 2. Se o Render estiver offline ou demorar, chama o motor de IA direto no app
      _useDirectIaFallback(prompt);
    }
  }

  void _useDirectIaFallback(String promptText) {
    final promptEncoded = Uri.encodeComponent(promptText);
    final directIaUrl = "https://image.pollinations.ai/prompt/$promptEncoded?model=video&nologo=true";
    _initializeVideoPlayer(directIaUrl);
  }

  void _initializeVideoPlayer(String url) {
    _videoController = VideoPlayerController.networkUrl(Uri.parse(url))
      ..initialize().then((_) {
        setState(() {
          _isLoading = false;
        });
        _videoController?.play();
      }).catchError((error) {
        setState(() {
          _errorMessage = "Erro ao processar o vídeo. Tente novamente com outro texto.";
          _isLoading = false;
        });
      });
  }

  @override
  void dispose() {
    _controller.dispose();
    _videoController?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Criador de Vídeo Automático'),
        backgroundColor: Colors.deepPurple,
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'O que você deseja criar hoje?',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _controller,
              maxLines: 3,
              decoration: InputDecoration(
                hintText: 'Ex: Um vídeo curto sobre a exploração espacial...',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                filled: true,
                fillColor: const Color(0xFF1E1E1E),
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _isLoading ? null : _generateVideo,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.deepPurple,
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              child: _isLoading
                  ? const SizedBox(
                      height: 24,
                      width: 24,
                      child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2),
                    )
                  : const Text('GERAR VÍDEO', style: TextStyle(fontSize: 16)),
            ),
            if (_errorMessage != null) ...[
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.red.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  _errorMessage!,
                  style: const TextStyle(color: Colors.redAccent),
                  textAlign: TextAlign.center,
                ),
              ),
            ],
            if (_videoController != null && _videoController!.value.isInitialized) ...[
              const SizedBox(height: 24),
              const Text(
                'Resultado:',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 12),
              AspectRatio(
                aspectRatio: _videoController!.value.aspectRatio,
                child: Container(
                  clipBehavior: Clip.antiAlias,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(12),
                    color: Colors.black,
                  ),
                  child: VideoPlayer(_videoController!),
                ),
              ),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  IconButton(
                    iconSize: 40,
                    icon: Icon(
                      _videoController!.value.isPlaying
                          ? Icons.pause_circle_filled
                          : Icons.play_circle_filled,
                      color: Colors.deepPurpleAccent,
                    ),
                    onPressed: () {
                      setState(() {
                        _videoController!.value.isPlaying
                            ? _videoController!.pause()
                            : _videoController!.play();
                      });
                    },
                  ),
                ],
              ),
            ],
          ],
        ),
      ),
    );
  }
}
