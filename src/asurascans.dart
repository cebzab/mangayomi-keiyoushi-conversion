// Mangayomi Extension
// name: AsuraScans
// lang: en
// type: manga
// version: 1
// nsfw: false

import 'package:mangayomi/extension_api.dart';

class AsuraScans extends MProvider {
  AsuraScans()
      : super(
          sourceName: "AsuraScans",
          baseUrl: "https://asuracomic.net",
          lang: "en",
          typeSource: SourceType.manga,
          iconUrl:
              "https://asuracomic.net/wp-content/uploads/2023/10/asura-logo.png",
        );

  @override
  Future<List<MangaModel>> getPopularManga(int page) async {
    final res = await http.get("$baseUrl/manga/?page=$page");
    final document = parseHtml(res);
    final elements = document.select("div.bsx");
    return elements.map((e) {
      final a = e.selectFirst("a");
      final title = a?.attr("title") ?? "";
      final url = a?.attr("href") ?? "";
      final img = e.selectFirst("img")?.attr("src") ?? "";
      return MangaModel(
        title: title,
        url: url,
        imageUrl: img,
      );
    }).toList();
  }

  @override
  Future<List<MangaModel>> searchManga(String query, int page) async {
    final res =
        await http.get("$baseUrl/page/$page/?s=${Uri.encodeQueryComponent(query)}");
    final document = parseHtml(res);
    final elements = document.select("div.bsx");
    return elements.map((e) {
      final a = e.selectFirst("a");
      final title = a?.attr("title") ?? "";
      final url = a?.attr("href") ?? "";
      final img = e.selectFirst("img")?.attr("src") ?? "";
      return MangaModel(
        title: title,
        url: url,
        imageUrl: img,
      );
    }).toList();
  }

  @override
  Future<MangaModel> getMangaDetails(String url) async {
    final res = await http.get(url);
    final document = parseHtml(res);
    final title = document.selectFirst("h1.entry-title")?.text ?? "";
    final img =
        document.selectFirst("div.thumb img")?.attr("src") ?? "";
    final desc = document
            .selectFirst("div.entry-content p")
            ?.text
            .trim() ??
        "";
    return MangaModel(
      title: title,
      url: url,
      imageUrl: img,
      description: desc,
    );
  }

  @override
  Future<List<ChapterModel>> getChapterList(String url) async {
    final res = await http.get(url);
    final document = parseHtml(res);
    final chapters = document.select("ul.clstyle li a");
    return chapters.map((a) {
      final name = a.text.trim();
      final link = a.attr("href") ?? "";
      return ChapterModel(name: name, url: link);
    }).toList();
  }

  @override
  Future<List<String>> getPageList(String url) async {
    final res = await http.get(url);
    final document = parseHtml(res);
    final imgs = document.select("div#readerarea img");
    return imgs.map((e) => e.attr("src") ?? "").toList();
  }
}