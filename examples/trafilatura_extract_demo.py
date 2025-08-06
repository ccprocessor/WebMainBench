import time
from webmainbench.extractors import ExtractorFactory

# 配置 Trafilatura 抽取器（这里可根据需要添加更多配置）
config = {}

try:
    # 创建 Trafilatura 抽取器实例
    extractor = ExtractorFactory.create("trafilatura", config=config)
    print(f"✅ Extractor创建成功: {extractor.description}")
    print(f"📋 版本: {extractor.version}")
    print(f"⚙️ 配置: {extractor.get_config()}\n")
except Exception as e:
    print(f"❌ Extractor创建失败: {e}")


# 测试 HTML
test_html = """
<html><head>
<style id="cc-extraStyle" name="cc">
        noscript {
          display: none !important;
        }
        .cc-unloaded:not(iframe) {
          width: 100px;
          height: 100px;
          background-color: #ffebeb;
          border: 2px dashed #ff0000;
        }
        .mark-selected {
            outline: 2px dashed #0d6efd !important;
            background-color: rgba(13, 110, 253, 0.1) !important;
        }
        .selecto-selection {
            background: rgba(13, 110, 253, 0.1);
            outline: 1px dashed #0d6efd;
        }
    </style>
<script async="" src="//www.i.cdn.cnn.com/zion/zion-mb.min.js" type="text/javascript"></script><title>Tracking Covid-19 vaccinations in the US</title><meta charset="utf-8"><meta content="index,follow" name="robots"><meta content="noarchive" name="googlebot"><meta content="Tracking Covid-19 vaccinations in the US" name="title"><meta content="Track each state’s progress as the US vaccination campaign gets underway" name="description"><meta content="coronavirus, novel coronavirus, covid-19, public health, maps, charts, vaccinations, vaccines" name="keywords"><meta content="" name="news_keywords"><meta content="CNN" name="source"><meta content="health" name="section"><meta content="" name="subsection"><meta content="CNN" name="application-name"><meta content="width=device-width,initial-scale=1,shrink-to-fit=no" name="viewport"><meta content="https://www.cnn.com/interactive/2021/health/us-covid-vaccinations/" property="og:url"><meta content="article" property="og:type"><meta content="CNN" property="og:site_name"><meta content="en_US" property="og:locale"><meta content="Tracking Covid-19 vaccinations in the US" property="og:title"><meta content="Track each state’s progress as the US vaccination campaign gets underway" property="og:description"><meta content="https://cdn.cnn.com/cnn/2021/images/05/21/20210521-us-vax-tracker_social-card.jpg" property="og:image"><meta content="A choropleth map of the United States' vaccination rates by region." property="og:image:alt"><meta content="690014395" property="fb:admins"><meta content="80401312489" property="fb:app_id"><meta content="@CNN" name="twitter:site"><meta content="759251" name="twitter:site:id"><meta content="@CNN" name="twitter:creator"><meta content="summary_large_image" name="twitter:card"><meta content="https://cdn.cnn.com/cnn/2021/images/05/21/20210521-us-vax-tracker_social-card.jpg" name="twitter:image"><meta content="" name="twitter:image:alt"><link href="https://www.cnn.com/interactive/2021/health/us-covid-vaccinations/" rel="canonical"><link href="../../../2020/health/coronavirus-us-dashboard-assets/images/favicon.ico" rel="shortcut icon"><link href="https://cdn.cnn.com/cnn/.e/img/3.0/global/misc/apple-touch-icon.png" rel="apple-touch-icon"><link href="https://rss.cnn.com/rss/cnn_topstories.rss" rel="alternate" title="CNN - Top Stories [RSS]"><link href="https://rss.cnn.com/rss/cnn_latest.rss" rel="alternate" title="CNN - Recent Stories [RSS]"><link href="https://edition.cnn.com" hreflang="en" rel="alternate" title="CNN International"><link href="https://arabic.cnn.com" hreflang="ar" rel="alternate" title="CNN Arabic"><link href="https://mexico.cnn.com" hreflang="es" rel="alternate" title="CNN Mexico"><link href="../../../2020/health/coronavirus-us-dashboard-assets/styles.css?v=200323603" rel="stylesheet"><script async="" src="//static.chartbeat.com/js/chartbeat.js" type="text/javascript"></script><script async="" src="https://vi.ml314.com/get?eid=64240&amp;tk=GBYTTE9dUG2OqHj1Rk9DPOaLspvMWfLqV236sdkHgf03d&amp;fp=3635753128989032462"></script><script async="" src="https://cdn.ml314.com/taglw.js"></script><script async="" src="https://sb.scorecardresearch.com/cs/6035748/beacon.js" type="text/javascript"></script><script async="" id="GPTScript" src="https://securepubads.g.doubleclick.net/tag/js/gpt.js" type="text/javascript"></script><script src="https://i.cdn.cnn.com/analytics/cnn/ais.js"></script><script src="https://i.cdn.cnn.com/ads/cnn/adfuel.js"></script><script>var editionRef = window.location.href.indexOf("edition") > 0  ? 'CNNI' : 'CNN';
        window[editionRef] = window[editionRef] || {};
        window[editionRef]['adTargets'] = window[editionRef]['adTargets'] || {};
        window[editionRef]['adTargets']['spec'] = '';

        window.CNN = window.CNN || {};
        window.CNN.staticResponsive = true;
        window.CNNSTATICSECTION = 'health';

        window.CNN.interactive = window.CNN.interactive || {};

        window.CNN.omniture =
        {
            "branding_ad_page":           "",
            "branding_ad_zone":           ["", "", ""],
            "branding_ad_container":      ["", "", ""],
            "branding_ad_card":           ["", "", ""],
            "branding_content_page":      "",
            "branding_content_zone":      ["", "", ""],
            "branding_content_container": ["", "", ""],
            "branding_content_card":      ["", "", ""],
            "cap_author":                 "",
            "cap_content_type":           "article",
            "cap_genre":                  "",
            "cap_franchise":              "",
            "cap_media_type":             "",
            "cap_show_name":              "",
            "cap_topic":                  "",
            "friendly_name":              "Tracking Covid-19 vaccinations in the US",
            "full_gallery":               "",
            "gallery_name":               "",
            "gallery_slide":              "",
            "grid_size":                  "",
            "headline":                   "Tracking Covid-19 vaccinations in the US",
            "ireport_assignment":         "",
            "publish_date":               "",
            "rs_flag":                    "",
            "search_results_count":       "",
            "search_results_page":        "",
            "search_term":                "",
            "section":                    ["world", "health", "interactives"],
            "template_type":              "interactive",
            "video_collection":           "",
            "video_hpt":                  "",
            "video_opportunity":          "",
            "video_player_type":          ""
        }</script><meta content="AlK2UR5SkAlj8jjdEc9p3F3xuFYlF6LYjAML3EOqw1g26eCwWPjdmecULvBH5MVPoqKYrOfPhYVL71xAXI1IBQoAAAB8eyJvcmlnaW4iOiJodHRwczovL2RvdWJsZWNsaWNrLm5ldDo0NDMiLCJmZWF0dXJlIjoiV2ViVmlld1hSZXF1ZXN0ZWRXaXRoRGVwcmVjYXRpb24iLCJleHBpcnkiOjE3NTgwNjcxOTksImlzU3ViZG9tYWluIjp0cnVlfQ==" http-equiv="origin-trial"><meta content="Amm8/NmvvQfhwCib6I7ZsmUxiSCfOxWxHayJwyU1r3gRIItzr7bNQid6O8ZYaE1GSQTa69WwhPC9flq/oYkRBwsAAACCeyJvcmlnaW4iOiJodHRwczovL2dvb2dsZXN5bmRpY2F0aW9uLmNvbTo0NDMiLCJmZWF0dXJlIjoiV2ViVmlld1hSZXF1ZXN0ZWRXaXRoRGVwcmVjYXRpb24iLCJleHBpcnkiOjE3NTgwNjcxOTksImlzU3ViZG9tYWluIjp0cnVlfQ==" http-equiv="origin-trial"><meta content="A9uiHDzQFAhqALUhTgTYJcz9XrGH2y0/9AORwCSapUO/f7Uh7ysIzyszNkuWDLqNYg8446Uj48XIstBW1qv/wAQAAACNeyJvcmlnaW4iOiJodHRwczovL2RvdWJsZWNsaWNrLm5ldDo0NDMiLCJmZWF0dXJlIjoiRmxlZGdlQmlkZGluZ0FuZEF1Y3Rpb25TZXJ2ZXIiLCJleHBpcnkiOjE3Mjc4MjcxOTksImlzU3ViZG9tYWluIjp0cnVlLCJpc1RoaXJkUGFydHkiOnRydWV9" http-equiv="origin-trial"><meta content="A9R+gkZL3TWq+Z7RJ2L0c7ZN7FZD5z4mHmVvjrPitg/EMz9P3j5d3W7Vw5ZR9jtJGmWKltM4BO3smNzpCgwYuwwAAACTeyJvcmlnaW4iOiJodHRwczovL2dvb2dsZXN5bmRpY2F0aW9uLmNvbTo0NDMiLCJmZWF0dXJlIjoiRmxlZGdlQmlkZGluZ0FuZEF1Y3Rpb25TZXJ2ZXIiLCJleHBpcnkiOjE3Mjc4MjcxOTksImlzU3ViZG9tYWluIjp0cnVlLCJpc1RoaXJkUGFydHkiOnRydWV9" http-equiv="origin-trial"><script async="" src="https://securepubads.g.doubleclick.net/pagead/managed/js/gpt/m202408010101/pubads_impl.js?cb=31085847"></script><script async="" src="https://fundingchoicesmessages.google.com/i/22876227373?ers=3"></script><script async="" src="https://fundingchoicesmessages.google.com/f/AGSKWxVA3GOw-6JxfZUPguNZVRj4B3WXcduXUryrXaH7pxbRK7UH5pdBIkScn5BGcuAmGkLOuzvBW-WeMj9OUPwSXQBRpqX1qboBWtnM0fT0JiqTAe39hHFyn7p6ss9jZJmNXis_8xtEew==?fccs=W1siQUtzUm9sX1dYM3pBMlo2Tkd4WUhMYnFpNmNFeTItTFJsY1RIaFA5NU81ZVdheG9wemRUTnpycktRRDdCR1czRGRKTlpiaTJPTjRWWk1QbXBHY3I2cnJLS2hTODVxUnBDeDFMa290cXRuNVphUV9TS01MRFQwSWFxMnp4ZHh0TmZ1VzdlcUNuMXN0QkFhSm9OcjNBQkJ3dnBzQlVYMk1TNTdRPT0iXSxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsWzE3MjI1ODc3NTEsMTk4MDAwMDAwXSxudWxsLG51bGwsbnVsbCxbbnVsbCxbN11dLCJodHRwczovL2VkaXRpb24uY25uLmNvbS9pbnRlcmFjdGl2ZS8yMDIxL2hlYWx0aC91cy1jb3ZpZC12YWNjaW5hdGlvbnMvIixudWxsLFtbOCwiOUFMT2VlSV9wbWciXSxbOSwiemgtQ04iXSxbMjIsInRydWUiXSxbMjAsIltudWxsLG51bGwsWzMxMDg0MTkxXSw1LDZdIl0sWzE5LCIyIl0sWzE3LCJbMF0iXV1d"></script><script async="" src="https://fundingchoicesmessages.google.com/f/AGSKWxVLopJd-q6kOk-6YP5TgzBHEbNVIfpRn-1twQ7vccqG0qZTaMiRMTtoVgQvb1Tft1wZ4-4036rlmfdUX_TWDWQmu3WTjvhJOdrMJG5tns2KW4F_IIFnBHlrllv8qmvlk7IUaSkIpw==?fccs=W1siQUtzUm9sX1dYM3pBMlo2Tkd4WUhMYnFpNmNFeTItTFJsY1RIaFA5NU81ZVdheG9wemRUTnpycktRRDdCR1czRGRKTlpiaTJPTjRWWk1QbXBHY3I2cnJLS2hTODVxUnBDeDFMa290cXRuNVphUV9TS01MRFQwSWFxMnp4ZHh0TmZ1VzdlcUNuMXN0QkFhSm9OcjNBQkJ3dnBzQlVYMk1TNTdRPT0iXSxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsWzE3MjI1ODc3NTEsMjY3MDAwMDAwXSxudWxsLG51bGwsbnVsbCxbbnVsbCxbNyw5XSxudWxsLDIsbnVsbCwiemgtQ04iXSwiaHR0cHM6Ly9lZGl0aW9uLmNubi5jb20vaW50ZXJhY3RpdmUvMjAyMS9oZWFsdGgvdXMtY292aWQtdmFjY2luYXRpb25zLyIsbnVsbCxbWzgsIjlBTE9lZUlfcG1nIl0sWzksInpoLUNOIl0sWzIyLCJ0cnVlIl0sWzIwLCJbbnVsbCxudWxsLFszMTA4NDE5MV0sNSw2XSJdLFsxOSwiMiJdLFsxNywiWzBdIl1dXQ"></script><script async="" src="https://lightning.cnn.com/launch/7be62238e4c3/97fa00444124/db1e395fbeab/EXb9b8027db27c4833867b28f4c02dbd16-libraryCode_source.min.js"></script><script async="" src="https://lightning.cnn.com/launch/7be62238e4c3/97fa00444124/db1e395fbeab/RCd0b30c7962584e319e9bd37beadd7b1a-source.min.js"></script><script async="" src="https://lightning.cnn.com/launch/7be62238e4c3/97fa00444124/db1e395fbeab/RC5a87a3c699d940a8bb3a2ae2990f1cda-source.min.js"></script><script async="" src="https://lightning.cnn.com/launch/7be62238e4c3/97fa00444124/db1e395fbeab/RC4bdaf299cda84938b90fba243192f4a1-source.min.js"></script><script async="" src="https://lightning.cnn.com/launch/7be62238e4c3/97fa00444124/db1e395fbeab/RC0f55d142cf324bfe96150fc9a20d8e8c-source.min.js"></script><meta content="AxjhRadLCARYRJawRjMjq4U8V8okQvSnrBIJWdMajuEkN3/DfVAcLcFhMVrUWnOXagwlI8dQD84FwJDGj9ohqAYAAABveyJvcmlnaW4iOiJodHRwczovL2dvb2dsZWFkc2VydmljZXMuY29tOjQ0MyIsImZlYXR1cmUiOiJGZXRjaExhdGVyQVBJIiwiZXhwaXJ5IjoxNzI1NDA3OTk5LCJpc1RoaXJkUGFydHkiOnRydWV9" http-equiv="origin-trial"><script async="" src="https://fundingchoicesmessages.google.com/f/AGSKWxUDBnO2JCyq3umZrkI1tkl4HfUDSySUWzXkdXtt1z6HhOipBmnKLozG9ER2XHjMYqru_VEhxsijeszmMXQMZU3ShmmWoJrvZfqIRfkL6ouDBUeflI4QvAXiI8vQKSPNZ89o_-JJtA==?fccs=W1siQUtzUm9sX1dYM3pBMlo2Tkd4WUhMYnFpNmNFeTItTFJsY1RIaFA5NU81ZVdheG9wemRUTnpycktRRDdCR1czRGRKTlpiaTJPTjRWWk1QbXBHY3I2cnJLS2hTODVxUnBDeDFMa290cXRuNVphUV9TS01MRFQwSWFxMnp4ZHh0TmZ1VzdlcUNuMXN0QkFhSm9OcjNBQkJ3dnBzQlVYMk1TNTdRPT0iXSxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsWzE3MjI1ODc3NTIsMTU3MDAwMDAwXSxudWxsLG51bGwsbnVsbCxbbnVsbCxbNyw5LDZdLG51bGwsMixudWxsLCJ6aC1DTiIsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLDFdLCJodHRwczovL2VkaXRpb24uY25uLmNvbS9pbnRlcmFjdGl2ZS8yMDIxL2hlYWx0aC91cy1jb3ZpZC12YWNjaW5hdGlvbnMvIixudWxsLFtbOCwiOUFMT2VlSV9wbWciXSxbOSwiemgtQ04iXSxbMjIsInRydWUiXSxbMjAsIltudWxsLG51bGwsWzMxMDg0MTkxXSw1LDZdIl0sWzE5LCIyIl0sWzE3LCJbMF0iXV1d"></script></head><body data-anno-uid="anno-uid-py2f8mgoo2" style="user-select: none;"><div class="nav light" data-anno-uid="anno-uid-rmu62fxto6o"><div class="nav__container" data-anno-uid="anno-uid-lu7glofdfm9"><div class="logo" data-anno-uid="anno-uid-ridszs28788"><div class="logo-links" data-anno-uid="anno-uid-usv9rn3urq"><a aria-label="CNN" class="logo-links__cnn" data-analytics="header_logo" data-anno-uid="anno-uid-8e4ful43vpg" href="https://e.newsletters.cnn.com/"><svg class="" data-anno-uid="anno-uid-yqqnglmz5t" viewBox="0 0 53.54 53.54" xmlns="http://www.w3.org/2000/svg"><g data-anno-uid="anno-uid-vy1laf2o9ds" data-name="<Group>"><path d="M0 0h53.54v53.54H0z" data-anno-uid="anno-uid-z462gfv5qqd" data-name="<Path>" fill="#c80000"></path><g data-anno-uid="anno-uid-jnsa3qj1lhq" data-name="<Group>" fill="#fff"><path d="M10.85 26.77a4.08 4.08 0 0 1 4.08-4.08H18v-2.32h-3.09a6.4 6.4 0 1 0 0 12.8h6a.65.65 0 0 0 .61-.61V20.71a1.39 1.39 0 0 1 1-1.37 1.53 1.53 0 0 1 1.74.83L28 26.64l3.63 6.26a.65.65 0 0 0 .7.41.47.47 0 0 0 .34-.48V20.71a1.39 1.39 0 0 1 1-1.37 1.53 1.53 0 0 1 1.73.83l3.48 6 3.9 6.73a.65.65 0 0 0 .7.41.47.47 0 0 0 .34-.48v-15.7h-2.27v9.34l-4.05-7c-2.5-4.15-7.12-2.47-7.12 1.17v5.83l-4.05-7c-2.46-4.18-7.11-2.45-7.11 1.15v9.58a.64.64 0 0 1-.64.65h-3.65a4.08 4.08 0 0 1-4.08-4.08z" data-anno-uid="anno-uid-vzwkop3zuc" data-name="<Path>"></path><path d="M44.79 17.13v15.7a1.38 1.38 0 0 1-1.38 1.42 1.59 1.59 0 0 1-1.41-.88l-3.91-6.74-3.48-6a.65.65 0 0 0-.61-.4.47.47 0 0 0-.33.48v12.12a1.39 1.39 0 0 1-1 1.37 1.53 1.53 0 0 1-1.74-.83l-3.69-6.27-3.75-6.46a.65.65 0 0 0-.7-.41.47.47 0 0 0-.34.48v11.85a1.57 1.57 0 0 1-1.53 1.53h-6a7.32 7.32 0 1 1 0-14.65H18v-2.31h-3.09a9.64 9.64 0 1 0 0 19.28H21a3.5 3.5 0 0 0 3.79-3.85v-5.5l4.05 7c2.46 4.18 7.11 2.45 7.11-1.15v-5.85L40 34c2.46 4.18 7.11 2.45 7.11-1.15V17.13h-2.32z" data-anno-uid="anno-uid-6aflmyt4zzo" data-name="<Path>"></path></g></g></svg> </a><a data-anno-uid="anno-uid-rbw46ytmho" href="https://cnn.com/health"><svg aria-hidden="true" class="health-logo-icon" data-anno-uid="anno-uid-vd2x1r9n17" fill="#0C0C0C" height="40px" viewBox="0 0 99.85 27.51" width="70px" xmlns="https://www.w3.org/2000/svg"><path d="M45.52 1.12a4.57 4.57 0 0 0-1.05.13 4.84 4.84 0 0 0-.13 1.08 4.79 4.79 0 0 0 4.73 4.85 4.58 4.58 0 0 0 1-.14A4.7 4.7 0 0 0 50.25 6a4.79 4.79 0 0 0-4.73-4.88zM52.56 4.6a1.51 1.51 0 0 1 .42.05 2.12 2.12 0 0 1 .05.44 2.16 2.16 0 0 1-2 2.07 1.86 1.86 0 0 1-.42 0 2 2 0 0 1 0-.43 2.24 2.24 0 0 1 1.95-2.13z" data-anno-uid="anno-uid-q0bikoy0wkb" fill="#37b34a"></path><path d="M28.16 27.51a9.19 9.19 0 0 1-6.85-3 9.92 9.92 0 0 1-2.8-7.07v-.27a10 10 0 0 1 2.93-6.88A8.62 8.62 0 0 1 28 7.66a9.32 9.32 0 0 1 6.86 2.69 9.69 9.69 0 0 1 2.9 6.89 1.47 1.47 0 0 1 0 .41 1.5 1.5 0 0 1-1.58 1.28H21.94a6.32 6.32 0 0 0 1.8 3.38 5.94 5.94 0 0 0 2 1.41 6.38 6.38 0 0 0 2.41.45 6.2 6.2 0 0 0 2.77-.67l.13-.07a6.4 6.4 0 0 0 2.29-2.1 1.57 1.57 0 0 1 1.09-.73h.23a1.7 1.7 0 0 1 1 .35 1.77 1.77 0 0 1 .62 1 .9.9 0 0 1 0 .25 1.6 1.6 0 0 1-.36 1.1l-.09.1a9.18 9.18 0 0 1-1.31 1.6 10 10 0 0 1-1.9 1.38 9.17 9.17 0 0 1-4.46 1.13zm6.08-11.89a6.34 6.34 0 0 0-.51-1.32 7.05 7.05 0 0 0-1.32-1.76 6.54 6.54 0 0 0-2-1.26 5.89 5.89 0 0 0-2.27-.45 6 6 0 0 0-4.29 1.75l-.32.3A6.51 6.51 0 0 0 22 15.62zm23 11.85a1.69 1.69 0 0 1-1.11-.47 1.91 1.91 0 0 1-.5-1.23v-.87a12.22 12.22 0 0 1-1.34 1 9 9 0 0 1-5 1.48 9.26 9.26 0 0 1-6.82-2.92 10 10 0 0 1-2.79-7.07 10.11 10.11 0 0 1 .71-3.8 10.57 10.57 0 0 1 2.06-3.22 8.79 8.79 0 0 1 6.68-2.78 9.43 9.43 0 0 1 7 2.76 9.94 9.94 0 0 1 2.79 7v8.35a1.72 1.72 0 0 1-.46 1.3 2 2 0 0 1-.54.37 1.57 1.57 0 0 1-.67.1zm-8-16.66a6 6 0 0 0-4.48 1.95 6.6 6.6 0 0 0-1.76 4.7 6.71 6.71 0 0 0 1.88 4.74 6.09 6.09 0 0 0 8.92 0 6.71 6.71 0 0 0 1.88-4.73 6.61 6.61 0 0 0-1.88-4.7 6 6 0 0 0-4.5-1.96zm48.98 16.62a1.63 1.63 0 0 1-1.16-.43 1.75 1.75 0 0 1-.33-.54 1.64 1.64 0 0 1-.12-.63V15.62a4.83 4.83 0 0 0-1.39-3.44A4.34 4.34 0 0 0 92 10.72a4.4 4.4 0 0 0-3.28 1.46 4.82 4.82 0 0 0-1.37 3.44v10.17a1.52 1.52 0 0 1-.58 1.21 1.39 1.39 0 0 1-1.09.46 1.56 1.56 0 0 1-1.16-.51 1.45 1.45 0 0 1-.45-1.13V1.66a1.62 1.62 0 0 1 .45-1.15A1.59 1.59 0 0 1 85.68 0a1.5 1.5 0 0 1 1.17.54 1.5 1.5 0 0 1 .46 1.12V9a6.89 6.89 0 0 1 .69-.45 7.47 7.47 0 0 1 3.77-1 7.75 7.75 0 0 1 5.77 2.3 8 8 0 0 1 2.29 5.74v10.2a1.91 1.91 0 0 1-.13.84l-.35.34a1.68 1.68 0 0 1-1.13.46zm-84.06 0A1.62 1.62 0 0 1 13 27a1.87 1.87 0 0 1-.33-.54 1.68 1.68 0 0 1-.12-.63V15.62a4.8 4.8 0 0 0-1.4-3.44 4.38 4.38 0 0 0-6.53 0 4.79 4.79 0 0 0-1.38 3.44v10.17A1.48 1.48 0 0 1 2.7 27a1.36 1.36 0 0 1-1.09.46 1.56 1.56 0 0 1-1.16-.51A1.5 1.5 0 0 1 0 25.79V1.66A1.66 1.66 0 0 1 .45.51 1.59 1.59 0 0 1 1.61 0a1.48 1.48 0 0 1 1.17.54 1.5 1.5 0 0 1 .46 1.12V9A8.17 8.17 0 0 1 4 8.55a5.5 5.5 0 0 1 1.6-.65h.11a7.34 7.34 0 0 1 2.07-.29 7.73 7.73 0 0 1 5.76 2.3 8.06 8.06 0 0 1 2.3 5.74v10.14a1.57 1.57 0 0 1-.18.75l.07.07-.43.39a1.65 1.65 0 0 1-1.14.43zm63.51 0a1.75 1.75 0 0 1-1-.34 10.51 10.51 0 0 1-4.17-8.13V1.69a1.7 1.7 0 0 1 .48-1.2A1.58 1.58 0 0 1 74.13 0a1.61 1.61 0 0 1 .63.12 1.49 1.49 0 0 1 .54.37 1.47 1.47 0 0 1 .35.55 1.84 1.84 0 0 1 .11.65v6.22h4.35a1.52 1.52 0 0 1 1.66 1.52 1.57 1.57 0 0 1-1.66 1.51h-4.35v7.8a7.09 7.09 0 0 0 .51 2.64 7.53 7.53 0 0 0 2.44 3.05 1.67 1.67 0 0 1 .69 1.21 1.58 1.58 0 0 1-.52 1.27 1.73 1.73 0 0 1-1.21.48zm-9.82-.07a1.72 1.72 0 0 1-1-.35 12.81 12.81 0 0 1-1.12-1 10.09 10.09 0 0 1-2.18-3.26 10.83 10.83 0 0 1-.75-3.86V1.67a1.74 1.74 0 0 1 .1-.61 1.55 1.55 0 0 1 .3-.57A1.73 1.73 0 0 1 64.4 0a1.67 1.67 0 0 1 .65.12 1.83 1.83 0 0 1 .53.34 1.59 1.59 0 0 1 .38.6 1.74 1.74 0 0 1 .1.61v17a7.38 7.38 0 0 0 .48 2.67 6.37 6.37 0 0 0 2.37 3.06 1.68 1.68 0 0 1 .66 1.18 1.6 1.6 0 0 1-.47 1.24 1.75 1.75 0 0 1-1.25.52z" data-anno-uid="anno-uid-84prce1xljr"></path></svg></a></div></div><div class="social-share nav-share" data-anno-uid="anno-uid-ui9e89c82qs"><a class="social-share__facebook social-share__icon" data-anno-uid="anno-uid-dtq4fxczlb" href="https://www.facebook.com/sharer/sharer.php?u=https://www.cnn.com/interactive/2021/health/us-covid-vaccinations/" style="margin-right: 5px; display: none;" target="_blank"><svg data-anno-uid="anno-uid-blqg723cbo" height="24px" width="24px"><use data-anno-uid="anno-uid-5oszl77f7y" xlink:href="#fbShare" xmlns:xlink="http://www.w3.org/1999/xlink"></use></svg> </a><a class="social-share__twitter social-share__icon" data-anno-uid="anno-uid-v3l69jc3dw" href="https://twitter.com/intent/tweet?text=Track%20each%20state%E2%80%99s%20progress%20as%20the%20US%20vaccination%20campaign%20gets%20underway&amp;url=https://www.cnn.com/interactive/2021/health/us-covid-vaccinations/" style="margin-right: 5px; display: none;" target="_blank"><svg data-anno-uid="anno-uid-89er3eu8m7e" height="24px" width="24px"><use data-anno-uid="anno-uid-vdig31jdfl" xlink:href="#twitterShare" xmlns:xlink="http://www.w3.org/1999/xlink"></use></svg> </a><a class="social-share__share social-share__icon" data-anno-uid="anno-uid-sfj0cuweet" href="#!" style="margin-right: 5px;"><svg data-anno-uid="anno-uid-froj2p5hn8" height="24px" width="24px"><use data-anno-uid="anno-uid-dys2aov8ysm" xlink:href="#nativeShare" xmlns:xlink="http://www.w3.org/1999/xlink"></use></svg></a></div></div></div><svg data-anno-uid="anno-uid-he58qiuovz7" style="position:absolute;width:0;height:0;visibility:hidden; display:none; pointer-events: none;" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><defs data-anno-uid="anno-uid-7nhsc0rdl89"><symbol data-anno-uid="anno-uid-6iqdzrve669" id="twitterShare" viewBox="0 0 64 64"><path d="M60,15.2c-2.1,0.9-4.3,1.5-6.6,1.7c2.4-1.4,4.2-3.6,5.1-6.1c-2.2,1.3-4.7,2.2-7.3,2.7 c-2.1-2.2-5.1-3.5-8.4-3.5c-6.3,0-11.5,5-11.5,11.1c0,0.9,0.1,1.7,0.3,2.5C22,23.2,13.6,18.8,7.9,12c-1,1.6-1.6,3.5-1.6,5.6 c0,3.9,2,7.3,5.1,9.2c-1.9-0.1-3.7-0.6-5.2-1.4v0.1c0,5.4,4,9.9,9.2,10.9c-1,0.3-2,0.4-3,0.4c-0.7,0-1.5-0.1-2.2-0.2 c1.5,4.4,5.7,7.6,10.7,7.7c-3.9,3-8.9,4.8-14.3,4.8c-0.9,0-1.8-0.1-2.7-0.2c5.1,3.2,11.1,5,17.6,5c21.1,0,32.7-16.9,32.7-31.6 c0-0.5,0-1,0-1.4C56.5,19.4,58.5,17.4,60,15.2" data-anno-uid="anno-uid-orhhuaxv048"></path></symbol><symbol data-anno-uid="anno-uid-ejc2yw0wvd" id="fbShare" viewBox="0 0 64 64"><path d="M56,5.1H8c-1.6,0-3,1.4-3,3v48.8c0,1.7,1.3,3,3,3h25.9V38.7h-7v-8.3h7v-6.1 c0-7.1,4.3-10.9,10.5-10.9c3,0,5.9,0.2,6.7,0.3v7.7h-4.7c-3.4,0-4.1,1.6-4.1,4v5h8.1l-1,8.3h-7v21.2H56c1.6,0,3-1.4,3-3V8.1 C59,6.4,57.7,5.1,56,5.1" data-anno-uid="anno-uid-qbhp9dajshn"></path></symbol><symbol data-anno-uid="anno-uid-aqi9ojca7ca" id="nativeShare" viewBox="0 0 64 64"><path d="M50,34.00005 C50,32.89605 50.896,32.00005 52,32.00005 C53.104,32.00005 54,32.89605 54,34.00005 L54,58.00005 C54,59.10405 53.104,60.00005 52,60.00005 L12,60.00005 C10.896,60.00005 10,59.10405 10,58.00005 L10,34.00005 C10,32.89605 10.896,32.00005 12,32.00005 C13.104,32.00005 14,32.89605 14,34.00005 L14,56.00005 L50,56.00005 L50,34.00005 Z M47.3867,18.38875 C47.8987,18.89475 48.1437,19.64575 47.9117,20.32275 C47.3677,21.91675 45.5277,22.20975 44.5067,21.20175 L33.9997,10.99975 L33.9997,43.99975 C33.9997,44.99975 32.9997,45.99975 31.9997,45.99975 C30.9997,45.99975 29.9997,44.99575 29.9997,43.99975 L29.9997,10.99975 L19.4417,21.20175 C18.5717,22.06075 17.1077,21.97575 16.3557,20.94575 C15.7657,20.13675 15.9397,19.00175 16.6537,18.29775 L30.3267,4.79775 C30.3267,4.79675 30.3267,4.79675 30.3277,4.79675 L30.5417,4.58575 C31.3327,3.80475 32.6157,3.80475 33.4067,4.58575 L33.6197,4.79675 C33.6197,4.79675 33.6207,4.79675 33.6207,4.79775 L47.3867,18.38875 Z" data-anno-uid="anno-uid-owbcmhgssri"></path></symbol><symbol data-anno-uid="anno-uid-uqctmfxo97q" id="scroll-arrow" preserveAspectRatio="xMidYMid meet" viewBox="0 0 21 44"><g data-anno-uid="anno-uid-8f0x04t9xg3" fill="none" fill-rule="evenodd"><path d="M10.333.432v40.995" data-anno-uid="anno-uid-cun2005y34" stroke="#FFF" stroke-width="2.88"></path><path d="M21 32.746L19.12 31l-8.621 9.242L1.88 31 0 32.746 10.499 44z" data-anno-uid="anno-uid-7s8maw5u8yr" fill="#FFF"></path></g></symbol><symbol data-anno-uid="anno-uid-7jfjfghv58x" id="scrollIcon" preserveAspectRatio="xMidYMid meet" viewBox="0 0 33 33"><path d="M8.116 0C5.379 0-.306 1.495.013 9.19.225 14.32 5.72 22.257 16.5 33 27.279 22.257 32.775 14.32 32.987 9.19 33.306 1.495 27.621 0 24.884 0c-2.736 0-5.447 1.296-8.384 5.487C13.563 1.296 10.852 0 8.116 0z" data-anno-uid="anno-uid-e11pbfv49ck" fill="#FFF" fill-rule="evenodd"></path></symbol><symbol data-anno-uid="anno-uid-mixc59enxb" id="loader" viewBox="20 20 100 100"><defs data-anno-uid="anno-uid-1x78wxfvvcd"><linearGradient data-anno-uid="anno-uid-y432lnis6o" id="loader_linearGradient-1" x1="50%" x2="50%" y1="0%" y2="100%"><stop data-anno-uid="anno-uid-1xrek83gmlc" offset="0%" stop-color="#FFFFFF"></stop><stop data-anno-uid="anno-uid-v8i9y89jars" offset="100%" stop-color="#262626"></stop></linearGradient></defs><g data-anno-uid="anno-uid-hghutt12xcv" fill="none" fill-rule="evenodd" stroke="none" stroke-width="1" transform="translate(22.000000, 22.000000)"><circle cx="48" cy="48" data-anno-uid="anno-uid-3z0de2dcvkx" r="48" stroke="url(#loader_linearGradient-1)" stroke-width="3"></circle></g></symbol><symbol data-anno-uid="anno-uid-vh0bi1galio" id="cnnlogo" preserveAspectRatio="xMidYMid meet" viewBox="0 0 500 500"><g data-anno-uid="anno-uid-i7b2xmh8tgq"><rect data-anno-uid="anno-uid-4ouap7sxqmy" fill="#cc0000 " height="500" width="500" x="0.3"></rect><g data-anno-uid="anno-uid-peszm2cfdtp"><path d="M106.1,249.9c0-19.7,16-38.5,35.6-38.5h29.1v-19.3h-29.3c-30.8,0-55.8,27-55.8,57.8
                c0,30.8,25,57.8,55.8,57.8H194c2.9,0,5.7-4.8,5.7-7.2V197.1c0-5.7,3.4-10.5,8.7-12c4.5-1.2,10.8,0,15.1,7.2
                c0.2,0.3,13,22.6,32.7,56.4c15.4,26.6,31.4,54.1,31.6,54.6c1.6,2.8,3.5,4.1,5.6,3.5c1.4-0.4,2.5-1.7,2.5-4.2V197.1
                c0-5.7,4-10.5,9.3-12c4.5-1.2,11,0,15.3,7.2c0.2,0.3,11.7,20,30.5,52.3c16.6,28.6,33.8,58.2,34.1,58.7c1.7,2.8,3,4.1,5.1,3.5
                c1.4-0.4,2-1.7,2-4.2V163.3H373v84.1c0,0-33.3-58.2-34.8-60.9c-21.5-36.5-61.5-21.4-61.5,10v50.9c0,0-33.3-58.2-34.8-60.9
                c-21.5-36.5-61.5-21.4-61.5,10v83.4c0,3-3.5,8.6-6.9,8.6h-31.8C122.1,288.4,106.1,269.6,106.1,249.9z" data-anno-uid="anno-uid-u8u2172ioer"></path><path d="M401.9,163.3v139.5c0,5.7-3.4,10.5-8.7,12c-1,0.3-1.9,0.4-3.1,0.4c-4,0-8.6-2-12-7.7
                c-0.2-0.3-13.6-23.5-34.1-58.8c-14.8-25.5-30-51.8-30.3-52.3c-1.6-2.8-3.5-4.1-5.6-3.6c-1.3,0.4-2.5,1.7-2.5,4.2v105.7
                c0,5.7-3.9,10.5-9.3,12c-4.5,1.2-11.1,0-15.3-7.2c-0.2-0.3-12.8-21.8-31.8-54.6c-15.9-27.5-32.5-55.9-32.8-56.4
                c-1.7-2.8-3-4.1-5.1-3.5c-1.4,0.4-2,1.7-2,4.2v103.4c0,7.1-8.2,16.8-15.3,16.8h-52.5c-35.2,0-63.9-32.2-63.9-67.4
                c0-35.2,28.7-67.4,63.9-67.4h29.3v-19.3h-29.3c-46.4,0-84.1,40.2-84.1,86.6c0,46.4,37.7,86.6,84.1,86.6h53c20.1,0,34-14.3,34-36.1
                v-48c0,0,33.2,58.2,34.8,60.9c21.5,36.5,61.5,21.4,61.5-10v-50.9c0,0,33.3,58.2,34.8,60.9c21.5,36.5,61.5,21.4,61.5-10V163.3
                H401.9z" data-anno-uid="anno-uid-g6c8u3m7gvc"></path></g></g></symbol></defs></svg><div data-anno-uid="anno-uid-qq2vipqsvc" id="ad_bnr_atf_01" style="margin-top: 0px;"></div><div data-anno-uid="anno-uid-4orvoqfesqn" data-page="us-vaccines" data-zion="us-covid-vaccinations" id="root"><nav class="tracker-nav-wrapper" data-anno-uid="anno-uid-0qfnczsvlx5l"><div class="tracker-nav ?utm_term=PRV-1617059932394ca76dd3d31be&amp;utm_source=cnn_What+Matters+for+March+29%2C+2021&amp;utm_medium=email&amp;utm_campaign=1617059932416&amp;bt_ee_preview=lniiCcUyS78tL%2Bofd3ksdBgl%2Btd731Asc5xFJ%2FeIuLyZy8pDcAPSA4%2FemSHH2%2FiJ&amp;bt_user_id_preview&amp;bt_ts_preview=1617059932416 is-minimal" data-anno-uid="anno-uid-y45x7lb6g2"><p class="tracker-nav__title" data-anno-uid="anno-uid-tvn3bngtwqo" style="">CNN's other Covid-19 trackers</p><ul data-anno-uid="anno-uid-alofe94oh9p"><li class="tracker-nav-item tracker-nav--intl-covid coronavirus-maps-and-cases" data-anno-uid="anno-uid-d4uobzy3ya6" style="padding-left: 0px;"><a data-anno-uid="anno-uid-2yqrfdflio5" href="../../../2020/health/coronavirus-maps-and-cases/" style="">Global cases and deaths</a></li><li class="tracker-nav-item tracker-nav--us-covid coronavirus-us-maps-and-cases" data-anno-uid="anno-uid-3z3l3r1fup9"><a data-anno-uid="anno-uid-tcr1uqk1hh" href="../../../2020/health/coronavirus-us-maps-and-cases/">US cases and deaths</a></li><li class="tracker-nav-item tracker-nav--intl-vax global-covid-vaccinations" data-anno-uid="anno-uid-9x0zzhmr31o"><a data-anno-uid="anno-uid-h70i7qvg1xw" href="../../../2021/health/global-covid-vaccinations/">Global vaccinations</a></li><li class="tracker-nav-item tracker-nav--us-vax us-covid-vaccinations" data-anno-uid="anno-uid-1t2dqvn4a0j"><a data-anno-uid="anno-uid-r86yx42lou" href="../../../2021/health/us-covid-vaccinations/">US vaccinations</a></li><li class="tracker-nav-item" data-anno-uid="anno-uid-hjx8n067z9" style="padding-right: 0px;"><a data-anno-uid="anno-uid-bbz2qelqaub" href="https://cnn.com/coronavirus-latest">Latest news</a></li></ul></div></nav><div class="cp-dashboard-container" data-anno-uid="anno-uid-4cqnr28bh5x"><div class="cp-dashboard cp-dashboard--us-vaccines cp-dashboard-ready mode--phablet mode--desktop" data-anno-uid="anno-uid-a2rivcotj0m"><div class="cp-dashboard-header" data-anno-uid="anno-uid-wg3mzvd460e"><h1 cc-select="true" class="cp-heading undefined mark-selected" data-anno-uid="anno-uid-kcfo9djj9if" style="">Tracking Covid-19 vaccines in the US</h1><p cc-select="true" class="standfirst mark-selected" data-anno-uid="anno-uid-vl6irmxxgn9" style="">Follow how many people have been vaccinated and who is being left out</p><p class="byline" data-anno-uid="anno-uid-cgq9r3mea78" style="">By Daniel Wolfe, Byron Manley and Priya Krishnakumar, CNN</p><p class="timestamp" data-anno-uid="anno-uid-aboup5ty1xh" style="">Last updated: March 20, 2023 at 2:03 p.m. ET</p></div><div class="cp-container cp-container--small" data-anno-uid="anno-uid-b7j8qc977qr"><div class="body-copy" data-anno-uid="anno-uid-qc62pog6s3d"><p cc-select="true" class="mark-selected" data-anno-uid="anno-uid-t8xojvdgv1" style="">Since vaccinations began in the United States, the federal government has deferred to states and territories on how, when and to whom they administer these shots. While no federal mandate exists, the Centers for Disease Control and Prevention has widely encouraged vaccinations.</p>
<p cc-select="true" class="mark-selected" data-anno-uid="anno-uid-r828xcw038e" style="">Here is how many doses have been administered in each state.</p>
</div></div><div class="cp-container cp-container--small" data-anno-uid="anno-uid-yqlkmq4mqek"><div class="cp-graphic" data-anno-uid="anno-uid-qqwdlqz7lhf" id="readout-heading"><span cc-select="true" class="select-graf mark-selected" data-anno-uid="anno-uid-0x388al9nzwr" style="">In</span><select class="cp-select cp-select--inline cp-select--thin" data-anno-uid="anno-uid-hg7k0xkbms"><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-t5t39y2378a" value="AK">Alaska</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-hmo5oeadvip" value="AL">Alabama</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-70apoyuy24o" value="AR">Arkansas</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-yue2xbfbwo" value="AZ">Arizona</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-kuziehkwj8" value="CA">California</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-c030tyjzixs" value="CO">Colorado</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-3n8ksy6kxna" value="CT">Connecticut</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-bl2j9n1be7e" value="DC">Washington, DC</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-oydx6yq92e" value="DE">Delaware</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-cmz4sp3x0yw" value="FL">Florida</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-ev9kbarx3bh" value="GA">Georgia</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-qtq3jel3679" value="HI">Hawaii</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-4wni0dblwtr" value="IA">Iowa</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-m8viv463yl" value="ID">Idaho</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-z9htwu27ef" value="IL">Illinois</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-b7pf54qpled" value="IN">Indiana</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-jtik0dx7j2" value="KS">Kansas</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-su55aledyr" value="KY">Kentucky</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-6s8ywxpjfwr" value="LA">Louisiana</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-14gv5e8phowg" value="MA">Massachusetts</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-7ghr9l924dr" value="MD">Maryland</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-cvu8hnego94" value="ME">Maine</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-5gh6upuijn6" value="MI">Michigan</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-lr6bdcqqalp" value="MN">Minnesota</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-et6wy5cc3dr" value="MO">Missouri</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-b2145syrio" value="MS">Mississippi</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-ft7tb4u4eiu" value="MT">Montana</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-vbnbhn10aqo" value="NC">North Carolina</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-bgjr17u1sa7" value="ND">North Dakota</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-1grtfz7291ki" value="NE">Nebraska</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-2b1r94v6vkv" value="NH">New Hampshire</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-x6tmhyfv76p" value="NJ">New Jersey</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-jp5b9omlbhr" value="NM">New Mexico</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-o38g7xs30x" value="NV">Nevada</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-59ci6catvua" value="NY">New York</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-fz24s36ax06" value="OH">Ohio</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-8rigvlfxfyb" value="OK">Oklahoma</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-m87hg7x5u5" value="OR">Oregon</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-d4kdczfyis" value="PA">Pennsylvania</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-0v13ig19dhj" value="PR">Puerto Rico</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-i9g1gvz63bs" value="RI">Rhode Island</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-de0ay7ujluc" value="SC">South Carolina</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-1lgpkaw257o" value="SD">South Dakota</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-uw484j4gviq" value="TN">Tennessee</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-uv09ee6tuy" value="TX">Texas</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-uvxz4q46a4o" value="UT">Utah</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-m6gunzrden" value="VA">Virginia</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-lpyj6mrnpm" value="VT">Vermont</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-6oixm54y7xl" value="WA">Washington</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-rs7dbctqzka" value="WI">Wisconsin</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-ht2zlsnb6s5" value="WV">West Virginia</option><option cc-select="true" class="mark-selected" data-anno-uid="anno-uid-dkid8nsx2eh" value="WY">Wyoming</option></select><div class="cp-vaccine-readout" data-anno-uid="anno-uid-jq6c75z81t"><p class="inline-graf" data-anno-uid="anno-uid-jtzxjpa2wu9"><span cc-select="true" class="highlight highlight-state mark-selected" data-anno-uid="anno-uid-chtb6cb2z8d" style="">7 million</span><span data-anno-uid="anno-uid-3ulykkvp0lr"><marked-text cc-select="true" class="mark-selected" data-anno-uid="anno-uid-i1s6cx1m7wo" style="">&nbsp;—&nbsp;or 56.99999999999999% — of the state’s&nbsp;</marked-text><span cc-select="true" class="highlight highlight-state mark-selected" data-anno-uid="anno-uid-ri0de8lljze">12.2 million doses</span></span><span cc-select="true" class="mark-selected" data-anno-uid="anno-uid-fjcyv9gs1cc">&nbsp;doses</span><marked-tail cc-select="true" class="mark-selected" data-anno-uid="anno-uid-qh9nfl0t1w" style="">&nbsp;have been administered.</marked-tail><span data-anno-uid="anno-uid-jz81dpvip6q"><marked-text cc-select="true" class="mark-selected" data-anno-uid="anno-uid-4gtuiv8cwa">&nbsp;That’s about&nbsp;</marked-text><span cc-select="true" class="highlight highlight-state mark-selected" data-anno-uid="anno-uid-xommfk0ryfc" style="">143 doses</span><marked-tail cc-select="true" class="mark-selected" data-anno-uid="anno-uid-covqkipgxmj" style="">&nbsp;for every hundred residents.</marked-tail></span><span data-anno-uid="anno-uid-lo2qanwnbn"><marked-text cc-select="true" class="mark-selected" data-anno-uid="anno-uid-rpwua3usa5b" style="">&nbsp;Roughly&nbsp;</marked-text><span cc-select="true" class="highlight highlight-state mark-selected" data-anno-uid="anno-uid-xe3tai722a" style="">53.2%</span><marked-tail cc-select="true" class="mark-selected" data-anno-uid="anno-uid-pr66sq57l3" style="">&nbsp;of residents are fully vaccinated.</marked-tail></span></p></div><div class="cp-vaccine-readout" data-anno-uid="anno-uid-70e7eznf6yy"><p data-anno-uid="anno-uid-ghl0ncsz2st"><marked-text cc-select="true" class="mark-selected" data-anno-uid="anno-uid-044xp83dw7es" style="">Across the country, about&nbsp;</marked-text><span cc-select="true" class="highlight highlight-us mark-selected" data-anno-uid="anno-uid-amqwx6blylu" style="">672.5 million doses</span><marked-tail cc-select="true" class="mark-selected" data-anno-uid="anno-uid-dvdozooehsg" style="">&nbsp;have been administered. That translates to&nbsp;</marked-tail><span cc-select="true" class="highlight highlight-us mark-selected" data-anno-uid="anno-uid-y5kc9fdwk6" style="">203 doses</span><marked-tail cc-select="true" class="mark-selected" data-anno-uid="anno-uid-fpwnsvujr1l" style="">&nbsp;per hundred people.</marked-tail></p></div></div></div><div class="cp-container cp-container--small" data-anno-uid="anno-uid-98zyq5u3ehp"><div class="body-copy" data-anno-uid="anno-uid-x6uehmpsy2"><p data-anno-uid="anno-uid-kp4o0y494nc"><marked-text cc-select="true" class="mark-selected" data-anno-uid="anno-uid-6hegmsu1wki" style="">President Joe Biden delivered on his promise of </marked-text><a cc-select="true" class="mark-selected" data-anno-uid="anno-uid-cpuhmmlfgs" href="https://www.cnn.com/2021/04/28/politics/president-biden-first-100-days/index.html" rel="nofollow" style="" target="_blank">200 million Covid-19 vaccin</a><a cc-select="true" class="mark-selected" data-anno-uid="anno-uid-803szppk2fp" href="https://www.cnn.com/2021/04/28/politics/president-biden-first-100-days/index.html" rel="nofollow" target="_blank">e doses</a> <a cc-select="true" class="mark-selected" data-anno-uid="anno-uid-kwymm914ruo" href="https://www.cnn.com/2021/04/28/politics/president-biden-first-100-days/index.html" rel="nofollow" target="_blank" style="">within his first 100 days</a><marked-tail cc-select="true" class="mark-selected" data-anno-uid="anno-uid-0kvdu94e8uj" style=""> in office. Administered doses peaked at over </marked-tail><a cc-select="true" class="mark-selected" data-anno-uid="anno-uid-wu7irgtqws" href="https://covid.cdc.gov/covid-data-tracker/#vaccination-trends" rel="nofollow" target="_blank">3</a> <a cc-select="true" class="mark-selected" data-anno-uid="anno-uid-s5i6aqj78nj" href="https://covid.cdc.gov/covid-data-tracker/#vaccination-trends" rel="nofollow" style="" target="_blank">million a day in April</a><marked-tail cc-select="true" class="mark-selected" data-anno-uid="anno-uid-m7xgmnqwzv" style="">. Eligibility for US residents grew after the Food and Drug Administration expanded emergency use authorization for the </marked-tail><a cc-select="true" class="mark-selected" data-anno-uid="anno-uid-5ok6wsvbft7" href="https://www.cnn.com/2021/05/10/health/pfizer-vaccine-eua-12-15-teens/index.html" rel="nofollow" style="" target="_blank">Pfizer vaccine to adolescents ages 12 to 15</a><marked-tail cc-select="true" class="mark-selected" data-anno-uid="anno-uid-z2ig416639o" style="">, then </marked-tail><a cc-select="true" class="mark-selected" data-anno-uid="anno-uid-axhdvyc4wxs" href="https://www.cnn.com/2021/11/02/health/covid-19-vaccine-children-acip/index.html" rel="nofollow" style="" target="_blank">a smaller dose for children ages</a> <a cc-select="true" class="mark-selected" data-anno-uid="anno-uid-8fs1jrul8x7" href="https://www.cnn.com/2021/11/02/health/covid-19-vaccine-children-acip/index.html" rel="nofollow" style="" target="_blank">5</a> <a cc-select="true" class="mark-selected" data-anno-uid="anno-uid-m8dt4panat" href="https://www.cnn.com/2021/11/02/health/covid-19-vaccine-children-acip/index.html" rel="nofollow" style="" target="_blank">to 11</a><marked-tail cc-select="true" class="mark-selected" data-anno-uid="anno-uid-hg0ay8v8q9" style="">, and authorization for booster shots from all three manufacturers cleared the way for millions more shots in arms. County-level data, however, shows </marked-tail><a cc-select="true" class="mark-selected" data-anno-uid="anno-uid-8furq5n1hz7" href="https://www.cnn.com/2021/04/18/us/covid-vaccine-slowing-us-demand/index.html" rel="nofollow" style="" target="_blank">just how far US communities have to go to reach herd immunity</a><marked-tail cc-select="true" class="mark-selected" data-anno-uid="anno-uid-tffepjjxepc" style="">.</marked-tail></p>
</div></div><div class="cp-container cp-container--large" data-anno-uid="anno-uid-l280eqsyrhn"><div data-anno-uid="anno-uid-69eprmwj85s"><div class="cp-graphic cp-graphic--large" data-anno-uid="anno-uid-dv79o3hbtd"><h3 cc-select="true" class="cp-heading cp-graphic__header mark-selected" data-anno-uid="anno-uid-4g6j0727nhe" style="">Vaccination progress in the United States</h3><div class="world-map-container metric-county" data-anno-uid="anno-uid-ck8sab72x57"><div class="cp-btn-options cp-btn-options--flex cp-btn-options--align-left" data-anno-uid="anno-uid-5lomvt5ik49" style="margin-bottom: 16px;"><div class="cp-btn-options__section" data-anno-uid="anno-uid-i4u4gvn9cjm"><button class="cp-btn cp-btn--option selected" data-anno-uid="anno-uid-xszp6gjt988" style="">By county</button><button class="cp-btn cp-btn--option" data-anno-uid="anno-uid-a4watoyfe6b" style="">By state</button></div></div><p cc-select="true" class="gray3 county-map__dek county-map__dek-- mark-selected" data-anno-uid="anno-uid-mp5co31jy" style="font-size: 13px;">Percentage of residents who are fully vaccinated</p><div class="vaccines-toggle-map-container" data-anno-uid="anno-uid-7bzkof11est"><div class="vaccines-toggle-map vaccines-toggle-map--show" data-anno-uid="anno-uid-i84v7llq9lq"><div class="cp-graphic cp-graphic--large cp-graphic--map-choropleth" data-anno-uid="anno-uid-8xfud70bgzk"><div class="overlay" data-anno-uid="anno-uid-pumwqt9gjnp"></div><div class="auto-container" data-anno-uid="anno-uid-nwrv8tkxfy"><div class="cp-autocomplete" data-anno-uid="anno-uid-94xevjt6p4w"><input data-anno-uid="anno-uid-wwlrrti1ik" id="auto" placeholder="E.g., Fort Bend County, Texas"></div><p class="choropleth-map-reset" data-anno-uid="anno-uid-f3jpvctft97" hidden=""><a data-anno-uid="anno-uid-y7hne5obzrn" href="#!"><svg aria-labelledby="replayIconTitle" cc-select="true" class="packages-cnn-icon-spec-storybook-styles__Icon--3LcUk replay-icon mark-selected" data-anno-uid="anno-uid-efnds9z10c" fill="currentColor" height="12" viewBox="0 -3 64 64" width="12" xmlns="https://www.w3.org/2000/svg"><path d="M32,4A27.79,27.79,0,0,0,15.38,9.46L13.13,6.81a1.69,1.69,0,0,0-3,.68L8.54,16.94a1.77,1.77,0,0,0,1.75,2H19.9a1.68,1.68,0,0,0,1.16-2.85l-.33-.39L18,12.52A24,24,0,1,1,8,32a2,2,0,0,0-4,0A28,28,0,1,0,32,4Z" data-anno-uid="anno-uid-thxu4cqm1nj"></path></svg><marked-tail cc-select="true" class="mark-selected" data-anno-uid="anno-uid-7xxo9s3tlj3"> Reset map</marked-tail></a></p></div><svg cc-select="true" class="choropleth-legend mark-selected" data-anno-uid="anno-uid-jn4wbff5mus" height="70px" preserveAspectRatio="xMinYMin meet" style="" viewBox="0 0 500 70" width="100%"></svg><svg cc-select="true" class="cp-states choropleth mark-selected" data-anno-uid="anno-uid-xl0oj2u4d9i" height="100%" id="choropleth-map" preserveAspectRatio="xMinYMin meet" style="" viewBox="0 20 700 460" width="100%"><pattern data-anno-uid="anno-uid-14j5qdgpzqw" height="4" id="diagonalHatch" patternUnits="userSpaceOnUse" width="4"><path d="M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2" data-anno-uid="anno-uid-fwzwhgrb9sk" style="stroke: rgba(0, 0, 0, 0.25); stroke-width: 1;"></path></pattern><g data-anno-uid="anno-uid-bmcqr52k1y" fill="none" transform="translate(0,0)"><g class="counties" data-anno-uid="anno-uid-8o1cjcpjvtk"></g><g class="states" data-anno-uid="anno-uid-ibvmcjgwomb"></g></g></svg><footer class="graphic-footer" data-anno-uid="anno-uid-3rydghmcm1n"><ul class="graphic-footer__list" data-anno-uid="anno-uid-jelk6bgosg"><li cc-select="true" class="graphic-footer__list-item mark-selected" data-anno-uid="anno-uid-rwx2duqdetk" style="">Last updated: December 9, 2022 at 5:56 p.m. ET</li><li class="graphic-footer__list-item" data-anno-uid="anno-uid-iv5f39u238"><marked-text cc-select="true" class="mark-selected" data-anno-uid="anno-uid-ll8f9vy2wlf" style="">Source: </marked-text><span data-anno-uid="anno-uid-eswbn7phpvp"><span data-anno-uid="anno-uid-3hmjm24yid6"><a cc-select="true" class="graphic-footer__link mark-selected" data-anno-uid="anno-uid-cjs3eu004hq" href="https://covid.cdc.gov/covid-data-tracker/#vaccinations" style="">Centers for Disease Control and Prevention</a></span></span><span data-anno-uid="anno-uid-15cybbisyaw"><span data-anno-uid="anno-uid-ibogu5j5tm"><marked-text cc-select="true" class="mark-selected" data-anno-uid="anno-uid-n1xtdmdr01c" style="">, </marked-text><a cc-select="true" class="graphic-footer__link mark-selected" data-anno-uid="anno-uid-jdbv8k7i7gs" href="https://tabexternal.dshs.texas.gov/t/THD/views/COVID-19VaccineinTexasDashboard/Summary" style="">Texas Department of State Health Services</a></span></span></li></ul></footer></div></div><div class="vaccines-toggle-map vaccines-toggle-map--hide" data-anno-uid="anno-uid-0tywg00smpgp"><div data-anno-uid="anno-uid-f7t3x7re7qi"><div class="cp-graphic cp-graphic--large no-breaking-text__" data-anno-uid="anno-uid-id648g54k5q"><div class="world-map-container metric-seriesCompletePopPct" data-anno-uid="anno-uid-y3tkka72cfh" id="us-vax-map"><div alt="This choropleth map of the United States shows vaccine administration by state." class="cp-graphic cp-graphic--large cp-graphic--map-choropleth" data-anno-uid="anno-uid-lim195wscmt"><div class="overlay overlay--states-map" data-anno-uid="anno-uid-xx5wqbmndis"></div><div class="choropleth-legend-container" data-anno-uid="anno-uid-yakgiwuuxj9"><svg aria-hidden="true" cc-select="true" class="choropleth-legend mark-selected" data-anno-uid="anno-uid-ulyk4y6tqv" height="70px" preserveAspectRatio="xMinYMin meet" style="" viewBox="0 0 500 70" width="100%"><g class="legendLog" data-anno-uid="anno-uid-6rwwygcyj93" transform="translate(0,2)"><g class="legendCells" data-anno-uid="anno-uid-oxck5dzwl5b"><g class="cell" data-anno-uid="anno-uid-qoqdksn6wfr" transform="translate(0,0)"><rect class="swatch" data-anno-uid="anno-uid-tkveq82r6dg" height="5" style="fill: rgb(185, 233, 237);" width="100"></rect><text cc-select="true" class="label mark-selected" data-anno-uid="anno-uid-ztqtrqvmc0o" style="text-anchor: middle;" transform="translate(50,
          23)">Less than 30%</text></g><g class="cell" data-anno-uid="anno-uid-mzjgcnuk98i" transform="translate(101,0)"><rect class="swatch" data-anno-uid="anno-uid-47l488beozm" height="5" style="fill: rgb(142, 188, 192);" width="100"></rect><text cc-select="true" class="label mark-selected" data-anno-uid="anno-uid-v1myrcsfen" style="text-anchor: middle;" transform="translate(50,
          23)">30 to 40%</text></g><g class="cell" data-anno-uid="anno-uid-24j7tz7weo5" transform="translate(202,0)"><rect class="swatch" data-anno-uid="anno-uid-jnw47qfffh" height="5" style="fill: rgb(103, 148, 152);" width="100"></rect><text cc-select="true" class="label mark-selected" data-anno-uid="anno-uid-3w01d90q42r" style="text-anchor: middle;" transform="translate(50,
          23)">40 to 50%</text></g><g class="cell" data-anno-uid="anno-uid-muvm9in2fus" transform="translate(303,0)"><rect class="swatch" data-anno-uid="anno-uid-kmtd117y5do" height="5" style="fill: rgb(66, 112, 115);" width="100"></rect><text cc-select="true" class="label mark-selected" data-anno-uid="anno-uid-u9h4hxgp7ah" style="text-anchor: middle;" transform="translate(50,
          23)">50 to 60%</text></g><g class="cell" data-anno-uid="anno-uid-9zliu3yimdn" transform="translate(404,0)"><rect class="swatch" data-anno-uid="anno-uid-hvv8599ccx" height="5" style="fill: rgb(28, 77, 80);" width="100"></rect><text cc-select="true" class="label mark-selected" data-anno-uid="anno-uid-udxklv990f" style="text-anchor: middle;" transform="translate(50,
          23)">60% or more</text></g></g></g></svg></div><svg aria-hidden="true" cc-select="true" class="cp-states choropleth mark-selected" data-anno-uid="anno-uid-5hp4hb4ieyo" height="100%" id="choropleth-map" preserveAspectRatio="xMinYMin meet" style="" viewBox="0 20 700 460" width="100%"><g data-anno-uid="anno-uid-1vzrdkw2d4q" fill="none" transform="translate(0,0)"><g class="states" data-anno-uid="anno-uid-h402ajem1ut"></g><g class="dc" data-anno-uid="anno-uid-7433dsfe69w" transform="translate(630,220)"><rect class="dc" data-anno-uid="anno-uid-62x49yepuac" data-color="#1c4d50" data-display-name="Washington, DC" data-doses-admin-per-100="298.21" data-doses-admin-total="2104626" data-series-complete-pop-pct="90.6" fill="#1c4d50" height="8" width="8" x="0" y="0"></rect><text cc-select="true" class="mark-selected" data-anno-uid="anno-uid-exn5z8w2wjw" fill="#262626" font-size="8px" x="10" y="7">DC</text></g></g></svg><footer class="graphic-footer" data-anno-uid="anno-uid-zi6ip9axio"><ul class="graphic-footer__list" data-anno-uid="anno-uid-71c2fojkwzf"><li cc-select="true" class="graphic-footer__list-item mark-selected" data-anno-uid="anno-uid-xah5ki8peda" style="">Last updated: March 10, 2023 at 1:56 p.m. ET</li><li class="graphic-footer__list-item" data-anno-uid="anno-uid-jlqwjj48rre"><marked-text cc-select="true" class="mark-selected" data-anno-uid="anno-uid-swpn66mq96h" style="">Source: </marked-text><span data-anno-uid="anno-uid-8hlnlojvyf2"><span data-anno-uid="anno-uid-tje0ewpziw8"><a cc-select="true" class="graphic-footer__link mark-selected" data-anno-uid="anno-uid-e3rx4yoij1p" href="https://covid.cdc.gov/covid-data-tracker/#vaccinations" style="">Centers for Disease Control and Prevention</a></span></span></li></ul></footer></div></div></div></div></div></div></div></div></div></div><div class="cp-container" data-anno-uid="anno-uid-dg1xqkbs60g"><div class="cp-graphic cp-graphic--multiline" data-anno-uid="anno-uid-hmftu0c1pg"><h3 cc-select="true" class="cp-heading cp-graphic__header mark-selected" data-anno-uid="anno-uid-hshk3a71f4s" style="">Vaccine doses administered per 100 people by state</h3><p cc-select="true" class="gray3 mark-selected" data-anno-uid="anno-uid-qqauyzmqi7" style="font-size: 13px;">Compare vaccine rollouts by state. Immunization rates are based on state population.</p><div class="tooltip" data-anno-uid="anno-uid-qcrrqqvfok"></div><div alt="This chart shows all 50 states, DC and Puerto Rico’s progress in administering the vaccine to their populations." class="graphic--svg-container" data-anno-uid="anno-uid-wyo8kwrsis"><svg aria-hidden="true" cc-select="true" class="cp-line-chart mark-selected" data-anno-uid="anno-uid-wnhveg13lbk" height="100%" id="vax-line-chart" style="" viewBox="0 0 780 450" width="100%"></svg></div><footer class="graphic-footer" data-anno-uid="anno-uid-fgzm92dd2sm"><ul class="graphic-footer__list" data-anno-uid="anno-uid-sg1qqni3dto"><li cc-select="true" class="graphic-footer__list-item mark-selected" data-anno-uid="anno-uid-y6ys7fo7zl" style="">Last updated: March 10, 2023 at 1:56 p.m. ET</li><li class="graphic-footer__list-item" data-anno-uid="anno-uid-d598g83y4uu"><marked-text cc-select="true" class="mark-selected" data-anno-uid="anno-uid-twtwxhtujed" style="">Source: </marked-text><span data-anno-uid="anno-uid-norocc51yej"><span data-anno-uid="anno-uid-so3adotre8"><a cc-select="true" class="graphic-footer__link mark-selected" data-anno-uid="anno-uid-qcjohj9uqnq" href="https://github.com/govex/COVID-19/tree/master/data_tables/vaccine_data" style="">Johns Hopkins University Centers for Civic Impact</a></span></span></li></ul></footer></div></div><div class="cp-container cp-container--small" data-anno-uid="anno-uid-b4o9iy3n0ql"><div class="body-copy" data-anno-uid="anno-uid-4kgik5d24oa"><p cc-select="true" class="mark-selected" data-anno-uid="anno-uid-704o7w1z1q9" style="">Demographic data about who is receiving the Covid-19 vaccine has revealed disparities between who is getting vaccinated and who is getting sick.</p>
<p data-anno-uid="anno-uid-apukoh6t6op"><marked-text cc-select="true" class="mark-selected" data-anno-uid="anno-uid-qlwaxpi9jtn" style="">Across nearly all states that have released demographic data, Black and Hispanic residents are getting vaccinated at </marked-text><a cc-select="true" class="mark-selected" data-anno-uid="anno-uid-4udmgj01zic" href="https://www.cnn.com/2021/01/26/us/vaccination-disparities-rollout/index.html" rel="nofollow" style="" target="_blank">lower rates than White people</a><marked-tail cc-select="true" class="mark-selected" data-anno-uid="anno-uid-9p8bni3e1y8" style="">, leading to concerns about </marked-tail><a cc-select="true" class="mark-selected" data-anno-uid="anno-uid-awvmpraqjea" href="https://www.cnn.com/2021/02/11/us/data-analysis-equitable-distribution-major-cities/index.html" rel="nofollow" style="" target="_blank">inequities in vaccine access</a> <a cc-select="true" class="mark-selected" data-anno-uid="anno-uid-othns9kmdy" href="https://www.cnn.com/2021/02/11/us/data-analysis-equitable-distribution-major-cities/index.html" rel="nofollow" style="" target="_blank">across the country</a><marked-tail cc-select="true" class="mark-selected" data-anno-uid="anno-uid-xibfxa1ro2">.</marked-tail></p>
</div></div><div class="cp-container" data-anno-uid="anno-uid-hhmzzkc9397"><div class="cp-graphic cp-graphic--multiline" data-anno-uid="anno-uid-hfgjk3d98e"><h3 cc-select="true" class="cp-heading cp-graphic__header mark-selected" data-anno-uid="anno-uid-b8688x616af" style="">Vaccine distribution by race and ethnicity</h3><p cc-select="true" class="gray3 mark-selected" data-anno-uid="anno-uid-5jl5ramcjtk" style="font-size: 13px;">Data from the CDC shows that minority populations are vaccinated at lower rates than their White peers. Only 171.7 million fully vaccinated people reported their ethnicity. Out of that group: More White people (55.7%) were fully vaccinated compared to Black (10.2%), Asian (7%) and Hispanic or Latino (19.8%) residents.</p><p cc-select="true" class="gray3 mark-selected" data-anno-uid="anno-uid-brmqham4v4" style="font-size: 13px;">The Kaiser Family Foundation, a national health policy nonprofit, collects data on these breakdowns for states sharing the race and ethnicity of those receiving vaccines.</p><div alt="This table shows the percentage of vaccinated people along their reported race and ethnicity. Not all states report these metrics, so it is an incomplete picture of the United States." class="region-table" data-anno-uid="anno-uid-q5d0dhzmc4o"><table class="cp-sortable-table" data-anno-uid="anno-uid-84styl034eq"><thead data-anno-uid="anno-uid-zd7rsiog5fq"><tr data-anno-uid="anno-uid-t5kqelzy8ph"><th class="name align-left valign-bottom sortable display-inline-block sorted asc" data-anno-uid="anno-uid-jbzk3cgh4y"><span cc-select="true" class="mark-selected" data-anno-uid="anno-uid-gm17stgkf68" style="">Location</span></th><th class="align-right valign-bottom sortable border-light data-col data-col-narrow" data-anno-uid="anno-uid-6tpcpqyq4vn"><span cc-select="true" class="mark-selected" data-anno-uid="anno-uid-ijjrbuwa5cc" style="">% Asian</span></th><th class="align-right valign-bottom sortable border-light data-col data-col-narrow" data-anno-uid="anno-uid-85j2khlg3wk"><span cc-select="true" class="mark-selected" data-anno-uid="anno-uid-4d7iq4k20ok" style="">% Black</span></th><th class="align-right valign-bottom sortable border-light data-col data-col-narrow" data-anno-uid="anno-uid-g9pg7llhrnw"><span cc-select="true" class="mark-selected" data-anno-uid="anno-uid-u3wsxgsa0ht">% Hispanic</span></th><th class="align-right valign-bottom sortable border-light data-col data-col-narrow" data-anno-uid="anno-uid-ms2ebg64z0m"><span cc-select="true" class="mark-selected" data-anno-uid="anno-uid-rq3ow78wjgf">% White</span></th></tr></thead><tbody data-anno-uid="anno-uid-k9tzepsz77b"><tr data-anno-uid="anno-uid-r2af2a01xkq"><td class="name align-left alabama" data-anno-uid="anno-uid-hhsmtods9aa"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-uckzcd844th" style="">Alabama</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-a32dhkpug3d" style="">2</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-llv4muc40br" style="">25</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-1wlgfmjq2db" style="">6</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-8lhgbbzevxb" style="">63</td></tr><tr data-anno-uid="anno-uid-tuvyrtza7kk"><td class="name align-left alaska" data-anno-uid="anno-uid-ztek6e98qf"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-9jl0iarrebm" style="">Alaska</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-8f8y675haow">7</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-wl7rg3lml" style="">3</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-69o69b2yxbi">6</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-w4zzyljqxj">56</td></tr><tr data-anno-uid="anno-uid-reny1z7jrjg"><td class="name align-left arizona" data-anno-uid="anno-uid-iqgvf19473"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-s9xngelsg">Arizona</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-qbqlqa5991g">4</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-xkyti5jzd7m" style="">3</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-5shb8n0369t" style="">19</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-kqbo6terjrd">51</td></tr><tr data-anno-uid="anno-uid-a93f3tnan4"><td class="name align-left arkansas" data-anno-uid="anno-uid-pqsae6k25zp"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-km7bs9xl9tn">Arkansas</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-x3odo4fn6o" style="">2</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-jxp79u9tq1j" style="">14</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-wsvznfhixz8" style="">7</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-6d495zdqp08">76</td></tr><tr data-anno-uid="anno-uid-lma4wqpksm"><td class="name align-left california" data-anno-uid="anno-uid-4iz2xv584fc"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-uslk5c0vekf">California</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-3xadi13r1h" style="">17</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-bwcv9bs8v0l" style="">4</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-w4e0gl0tu19">31</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-orks8t2cr6b">36</td></tr><tr data-anno-uid="anno-uid-ogtubsn6i1"><td class="name align-left colorado" data-anno-uid="anno-uid-azhfyfqtpmb"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-tej2x8hkah">Colorado</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-l94n7thyyer" style="">3</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-w0hjr3wbe2h" style="">4</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-krwjm2py1y" style="">13</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-afadtckwn2l">75</td></tr><tr data-anno-uid="anno-uid-11mtl1vm8v1i"><td class="name align-left connecticut" data-anno-uid="anno-uid-0avsrqjng4m"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-80r3bp2e9cd">Connecticut</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-qe06cl0pdz" style="">5</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-d2lw9wky5fj" style="">8</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-b1sc6tim5vr">15</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-sjjtywk8oqo">65</td></tr><tr data-anno-uid="anno-uid-8dmx26t7zlf"><td class="name align-left delaware" data-anno-uid="anno-uid-xqumt0kb0er"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-20qwpgwzfua">Delaware</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-vh2waywt8th" style="">4</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-qt5v3cb5xon" style="">17</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-x4epopdzp4">10</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-vyk75esj5eo">61</td></tr><tr data-anno-uid="anno-uid-5qk7rfe9k83"><td class="name align-left district-of-columbia" data-anno-uid="anno-uid-y96ptspnaf"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-s1u6j4pe9c">District of Columbia</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-xbmkwbtzi4r" style="">6</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-jy4w8zn4h4r" style="">45</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-6bm9ks42dhd" style="">14</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-ovnl7vbukm">49</td></tr><tr data-anno-uid="anno-uid-vhyq01hxfb"><td class="name align-left florida" data-anno-uid="anno-uid-702bq2ft0ws"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-68zhf3xtayq">Florida</span></td><td class="numeric align-right border-light data-col-narrow" data-anno-uid="anno-uid-9zw0xjhgt1n"></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-f7rihkui42" style="">9</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-pqccdv0hjt8">33</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-aa4ojmg1kg">53</td></tr><tr data-anno-uid="anno-uid-6q2qetv8z2"><td class="name align-left georgia" data-anno-uid="anno-uid-2bygm59lmz5"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-3svt45039d7">Georgia</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-b960wze8v2j" style="">6</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-9njd7uzujk" style="">27</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-qzah3ieiau" style="">9</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-t75tyd7dxd">53</td></tr><tr data-anno-uid="anno-uid-rsuqfc22pd"><td class="name align-left hawaii" data-anno-uid="anno-uid-iq8jnz5ju2s"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-t3a2qzvsau">Hawaii</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-hk7irdxmgj" style="">54</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-qlwy0ugqfeq" style="">1</td><td class="numeric align-right border-light data-col-narrow" data-anno-uid="anno-uid-r4nzf6jj3rk"></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-cut2j1qofr">26</td></tr><tr data-anno-uid="anno-uid-8qi6umi8drh"><td class="name align-left idaho" data-anno-uid="anno-uid-2ha7edqh95b"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-tvz96ordpsf">Idaho</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-lt7ynj6n58n">2</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-0mekt4v2w7ig" style="">1</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-g309c46967i" style="">11</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-o1af6v8cr6c">82</td></tr><tr data-anno-uid="anno-uid-kyjesikd8ni"><td class="name align-left illinois" data-anno-uid="anno-uid-f6l485zi886"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-1hqljj3qemt">Illinois</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-bnhx8d4abto">7</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-fvl3qhafm8i" style="">11</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-t4au4761xv" style="">15</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-9z6rmo9cjj">63</td></tr><tr data-anno-uid="anno-uid-geweqerjxzb"><td class="name align-left indiana" data-anno-uid="anno-uid-q0gr5zoutrj"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-9t27sd5ao3o">Indiana</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-jsq13gr60x">3</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-1f5cpus2hme" style="">7</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-miy40k3nrsq" style="">7</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-45dcolfhewj">80</td></tr><tr data-anno-uid="anno-uid-170umpnxv7n"><td class="name align-left iowa" data-anno-uid="anno-uid-20jy2qfxc2u"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-tcvo1eg5sy">Iowa</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-491g951yk69">2</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-gn6ll5fztqt" style="">2</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-3tuhl1yv5ki" style="">5</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-rmthacwv2xa">93</td></tr><tr data-anno-uid="anno-uid-lryfsah0wi"><td class="name align-left kansas" data-anno-uid="anno-uid-l2rxolwy2r"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-hnhut8l7z7a">Kansas</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-4nv1bqncs9o">3</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-hkze9xip8cb" style="">4</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-lgsqz3tzyom" style="">12</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-bkngrx0nmg">75</td></tr><tr data-anno-uid="anno-uid-o9i1aucwv1"><td class="name align-left kentucky" data-anno-uid="anno-uid-nuyg8a79m"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-i5hxxuut88a">Kentucky</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-qb8d40u6nl">2</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-3jj2uauu72m">7</td><td class="numeric align-right border-light data-col-narrow" data-anno-uid="anno-uid-v029a1ymqg"></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-wddcolqee5">81</td></tr><tr data-anno-uid="anno-uid-au5bdsku6rp"><td class="name align-left louisiana" data-anno-uid="anno-uid-sq7jm44yoap"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-m6prbsgv65">Louisiana</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-t9y6aei9dp9">3</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-xrtt5pp9hj">31</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-8cl903n9hg" style="">7</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-nstrbovngi">58</td></tr><tr data-anno-uid="anno-uid-gytz1z6r0a5"><td class="name align-left maine" data-anno-uid="anno-uid-zd7kx6dra0f"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-qilof2fh3n">Maine</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-p6by02x0kl">2</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-l0raw9l7k9">2</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-hk1sk0jk2c" style="">2</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-dptlc8p8e2d">82</td></tr><tr data-anno-uid="anno-uid-70tz7h3tw6"><td class="name align-left maryland" data-anno-uid="anno-uid-est9g61bggv"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-blj1v4x58j8">Maryland</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-hwk4815qtg">7</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-i0mf8ujyam">27</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-ome5btut6nj" style="">10</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-8h41t1gx1ld">54</td></tr><tr data-anno-uid="anno-uid-8wq055ryaun"><td class="name align-left massachusetts" data-anno-uid="anno-uid-og3ilm0htm"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-64lrt4ao2e2">Massachusetts</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-ka7jsaf4irj">8</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-0021fgjvstgxx">7</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-2ot007mcqh" style="">10</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-b957nwnnwtp">73</td></tr><tr data-anno-uid="anno-uid-yi6320r297l"><td class="name align-left michigan" data-anno-uid="anno-uid-cikbee7u5dn"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-x2gte8hvyok">Michigan</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-wel5i01kzf">4</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-ek0puwblj2q">10</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-nfwnldgq2tp" style="">5</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-4ge684tbejk">73</td></tr><tr data-anno-uid="anno-uid-prnpzvf3ize"><td class="name align-left minnesota" data-anno-uid="anno-uid-tawuafg8lo"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-831cow2rn6p">Minnesota</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-upoog9z99z">6</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-38f8dcyhztu">5</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-09s7glz0axfh" style="">5</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-1tk28yd7007">82</td></tr><tr data-anno-uid="anno-uid-t372vbkqj8a"><td class="name align-left mississippi" data-anno-uid="anno-uid-9ttraynnwic"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-0athis336pep">Mississippi</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-8kysbjn1eo4">2</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-ozuz9haii9">38</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-ei3ajg4fowu" style="">3</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-zwj0cvcvq5">56</td></tr><tr data-anno-uid="anno-uid-051si0qu8vxh"><td class="name align-left missouri" data-anno-uid="anno-uid-1n9ltm9b09z"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-hxtux2cl0mo">Missouri</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-z88cq0037ts">3</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-wmfgrvm9tne" style="">11</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-mv2eum2j3a" style="">5</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-k1erny09wea">86</td></tr><tr data-anno-uid="anno-uid-112k7zf3mm8"><td class="name align-left nevada" data-anno-uid="anno-uid-yfp4edjo8k"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-94st5n4uqu4">Nevada</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-wa8a4mb2dym">10</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-j2ilbszqj9">6</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-tnd3xnbia0l" style="">27</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-aza6m8dwrvk">39</td></tr><tr data-anno-uid="anno-uid-5cvqhiea549"><td class="name align-left new-hampshire" data-anno-uid="anno-uid-g11e3dwtz7k"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-tqln8ch635f">New Hampshire</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-rl6d8gnam3h">3</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-nb8c9npt53q">1</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-d0tkc56wdub" style="">3</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-3p2ehgcax3r">88</td></tr><tr data-anno-uid="anno-uid-ld52mzmku3"><td class="name align-left new-jersey" data-anno-uid="anno-uid-bua8ojzzy7"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-xzk159ymtzn">New Jersey</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-q3saqf7w9wa">11</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-hu11pqkibb">9</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-vys5yjimcrj" style="">18</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-spq4afkkjv8">51</td></tr><tr data-anno-uid="anno-uid-5q9kidyau2m"><td class="name align-left new-mexico" data-anno-uid="anno-uid-tm7zkhi1mr"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-qq6cssmerxi">New Mexico</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-ing3ck2l1i">3</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-4224q8pcedi">2</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-cuczzyi1unn" style="">40</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-ne1geshdio">42</td></tr><tr data-anno-uid="anno-uid-0eatpbv6dwl"><td class="name align-left new-york" data-anno-uid="anno-uid-dpnmqu8llq"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-xt0nny1kvv">New York</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-i4cqz7jg3g">14</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-ctgnkeyoj1i">15</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-9a2m1km5xbc" style="">21</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-jom1ifngpi">69</td></tr><tr data-anno-uid="anno-uid-v6h1db0k0xs"><td class="name align-left north-carolina" data-anno-uid="anno-uid-vx58a27py1r"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-5qtzco1e6qn">North Carolina</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-dz0k7d4qx6q">4</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-5akvv1q9zi">20</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-4mrgfw59qqr" style="">10</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-9tuih9ksvt">68</td></tr><tr data-anno-uid="anno-uid-m9esn3godvd"><td class="name align-left ohio" data-anno-uid="anno-uid-6iusabaakk5"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-rhe4igtp25i">Ohio</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-2gt6m46co3p">3</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-wpzcxoju8mi">10</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-hgwzt4inkn8" style="">4</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-c4xnmrh87a">78</td></tr><tr data-anno-uid="anno-uid-mnnidebloui"><td class="name align-left oklahoma" data-anno-uid="anno-uid-y7j3rlfz6l9"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-wknbu29r6xa">Oklahoma</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-gfih3uf404b">4</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-2ogswpi15u">7</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-vi12jsai38h" style="">12</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-7zyfh1gduir" style="">77</td></tr><tr data-anno-uid="anno-uid-g7sia1zbz9"><td class="name align-left oregon" data-anno-uid="anno-uid-mf99yh6njq"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-cwac7dxejug">Oregon</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-bz5xcy05mi">6</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-1hloyefuwuk" style="">3</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-pdskp9v12e" style="">10</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-t5ki9vfw2uf" style="">74</td></tr><tr data-anno-uid="anno-uid-ursl0pk9iv"><td class="name align-left pennsylvania" data-anno-uid="anno-uid-p8deq2mmvni"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-oya67q0l8g">Pennsylvania*</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-m6u3em9yd3n">2</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-aabkseilprh">6</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-boy8megaug9">7</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-xxkbz9sfme9" style="">79</td></tr><tr data-anno-uid="anno-uid-ihto2wdil"><td class="name align-left rhode-island" data-anno-uid="anno-uid-acfluckt0np"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-i6r24lpfy8p">Rhode Island</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-xt2o9y42n09">4</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-0iv0nrehv4sw">5</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-cg58su8xkhg">16</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-w3ide3djt9c" style="">75</td></tr><tr data-anno-uid="anno-uid-1qwfhcsi6jt"><td class="name align-left south-carolina" data-anno-uid="anno-uid-c5iuaei1gan"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-u4kto2lnor">South Carolina</span></td><td class="numeric align-right border-light data-col-narrow" data-anno-uid="anno-uid-korl274nua"></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-qaeoshk6zh" style="">22</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-cwlh03wp2gr">6</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-o9m3g2xw6t" style="">59</td></tr><tr data-anno-uid="anno-uid-mvqnr2nrwut"><td class="name align-left south-dakota" data-anno-uid="anno-uid-jds4vfsn58"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-zdbxfef0ki">South Dakota</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-sn7102ijebk">&lt;0.01</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-v7gc4ji9qg">1</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-qxnchu4ekv">&lt;0.01</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-6zn6p86wllp" style="">92</td></tr><tr data-anno-uid="anno-uid-xwkg8kx1ex"><td class="name align-left tennessee" data-anno-uid="anno-uid-dmhsw7xgo6"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-jeb65pse0kr">Tennessee</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-10wkqbji30v">2</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-c3cbiubg4q5" style="">12</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-lb4vhx139d">6</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-3hncu2gkrhh">63</td></tr><tr data-anno-uid="anno-uid-d1fgcdd1ha7"><td class="name align-left texas" data-anno-uid="anno-uid-v89fvx81lxg"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-q2kpseooqlm">Texas</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-5y0iovvhhmv">6</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-7hhd8mwk4jj">8</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-7tsojimy9bt">36</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-xdyvjf22mf8">36</td></tr><tr data-anno-uid="anno-uid-4hyviawo145"><td class="name align-left utah" data-anno-uid="anno-uid-tz497ikuqte"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-0rhj52hg1nh">Utah</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-4ok6ktbxemf">3</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-9xg462f7glh">1</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-jrwut1le1z">12</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-jvv79az7h2g">78</td></tr><tr data-anno-uid="anno-uid-xsvkbyhc7x"><td class="name align-left vermont" data-anno-uid="anno-uid-5u5nnpvo7c"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-2xagv7b602m">Vermont</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-8v573qzrleh">2</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-x814880ven">1</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-5xfokvd2dgd" style="">2</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-uej7c1a5v2s">95</td></tr><tr data-anno-uid="anno-uid-56uqhwn0065"><td class="name align-left virginia" data-anno-uid="anno-uid-1v36njf9nec"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-nwfz19pw7h">Virginia</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-579amcmeq4r">9</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-97bgnntof6">17</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-sddfpdie2g">10</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-io9whrbrcvs">58</td></tr><tr data-anno-uid="anno-uid-c6mdd7np67i"><td class="name align-left washington" data-anno-uid="anno-uid-zekp44y1w9q"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-jfvtgy8c1b">Washington</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-7jaallectng">11</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-ghu8shqvexj">4</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-tpnr2fad72b">11</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-i02q51y5cc">62</td></tr><tr data-anno-uid="anno-uid-czbx4f9vfjr"><td class="name align-left west-virginia" data-anno-uid="anno-uid-c4abfv24t77"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-q0odphejpxb">West Virginia</span></td><td class="numeric align-right border-light data-col-narrow" data-anno-uid="anno-uid-xxdb4ucvldh"></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-mn847xrwlk">3</td><td class="numeric align-right border-light data-col-narrow" data-anno-uid="anno-uid-obkq91x2gqn"></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-krutopie0rn" style="">90</td></tr><tr data-anno-uid="anno-uid-ul7bu9q9z5c"><td class="name align-left wisconsin" data-anno-uid="anno-uid-ya9y4e5ezo"><span cc-select="true" class="truncate mark-selected" data-anno-uid="anno-uid-8fiovjxicux">Wisconsin</span></td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-vcz72rmv48">4</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-1bnkfz6td7g">5</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-5tyki5dyyup">6</td><td cc-select="true" class="numeric align-right border-light data-col-narrow mark-selected" data-anno-uid="anno-uid-h4cqm1679n8" style="">90</td></tr></tbody></table></div><footer class="graphic-footer" data-anno-uid="anno-uid-mhj02kwdbec"><ul class="graphic-footer__list" data-anno-uid="anno-uid-6tegoeqz8et"><li cc-select="true" class="graphic-footer__list-item padding-bottom-item mark-selected" data-anno-uid="anno-uid-6pz5lr4ybxb" style="">* Does not include Philadelphia County due to differences in reporting data.</li><li cc-select="true" class="graphic-footer__list-item padding-bottom-item mark-selected" data-anno-uid="anno-uid-cpjw2lekljk" style="">Note: Percentages are based on total vaccinations for which race or ethnicity is known. Persons of Hispanic origin may be of any race. States vary in whether they include or exclude Hispanic individuals in racial categories. Additionally, some states vary in whether they include or exclude Hispanic individuals in racial categories in their reporting of vaccination data and in their reporting of cases and deaths. Some states use different racial classifications for their vaccination data and their reporting of cases and deaths. Shares of people vaccinated in each state may not sum to 100% due to rounding, pending or missing data. Vaccination data may not be directly comparable due to differences in data reported, reporting period, racial or ethnic classifications and rates of unknown race or ethnicity.</li><li class="graphic-footer__list-item" data-anno-uid="anno-uid-s85w7tgabgb"><marked-text cc-select="true" class="mark-selected" data-anno-uid="anno-uid-gle7lr97w2i" style="">Source: </marked-text><a cc-select="true" class="graphic-footer__link mark-selected" data-anno-uid="anno-uid-mcx070p6fp" href="https://www.kff.org/coronavirus-covid-19/issue-brief/state-covid-19-data-and-policy-actions/#raceethnicity" style="">Kaiser Family Foundation</a></li><li cc-select="true" class="graphic-footer__list-item mark-selected" data-anno-uid="anno-uid-v5uz3hmmbu" style="">Last updated: October 22, 2021 at 12:12 p.m. ET</li></ul></footer></div></div><p class="cp-dashboard-footer" data-anno-uid="anno-uid-k7ee7ygdcb"></p><section class="cp-methodology" data-anno-uid="anno-uid-x3wml644u7s"><h3 cc-select="true" class="cp-heading undefined mark-selected" data-anno-uid="anno-uid-0d2psjbbqd57" style="">About the data</h3><p data-anno-uid="anno-uid-0v3c1b0ft2h"></p><p data-anno-uid="anno-uid-17633zulz6g"><marked-text cc-select="true" class="mark-selected" data-anno-uid="anno-uid-psuk9q2qaui" style="">Most county-level vaccination data comes from the Centers for Disease Control and Prevention’s </marked-text><a cc-select="true" class="mark-selected" data-anno-uid="anno-uid-ltnmufdcdwi" href="https://covid.cdc.gov/covid-data-tracker/#county-view" rel="nofollow" style="" target="_blank">Covid Data Tracker</a><marked-tail cc-select="true" class="mark-selected" data-anno-uid="anno-uid-6f84e240tn">. Texas’ county-level data is from the </marked-tail><a cc-select="true" class="mark-selected" data-anno-uid="anno-uid-omphy31i9op" href="https://tabexternal.dshs.texas.gov/t/THD/views/COVID-19VaccineinTexasDashboard/VaccineDosesAllocated?%3Aorigin=card_share_link&amp;%3Aembed=y&amp;%3AisGuestRedirectFromVizportal=y" rel="nofollow" style="" target="_blank">Texas Department of State Health Services</a><marked-tail cc-select="true" class="mark-selected" data-anno-uid="anno-uid-98dfzpvquk4">.</marked-tail></p>
</section><p data-anno-uid="anno-uid-04ct5imji46"></p><p data-anno-uid="anno-uid-31x1qij7whl"></p><p data-anno-uid="anno-uid-t1f8walrdm"><marked-text cc-select="true" class="mark-selected" data-anno-uid="anno-uid-pp688jww02i" style="">Vaccination data for the line chart comes from Johns Hopkins University’s Centers for Civic Impact. More detailed information about JHU’s sourcing is available on </marked-text><a cc-select="true" class="mark-selected" data-anno-uid="anno-uid-2z8m8nhh6fj" href="https://github.com/govex/COVID-19/tree/master/data_tables/vaccine_data" rel="nofollow" style="" target="_blank">its GitHub repository</a><marked-tail cc-select="true" class="mark-selected" data-anno-uid="anno-uid-8e0ve9o587l">.</marked-tail></p>
<p data-anno-uid="anno-uid-ic735w2o0j"></p><p data-anno-uid="anno-uid-431c99e6fb4"><a cc-select="true" class="mark-selected" data-anno-uid="anno-uid-answs5i2834" href="https://www.kff.org/other/state-indicator/covid-19-vaccinations-by-race-ethnicity/?currentTimeframe=0&amp;sortModel=%7B%22colId%22:%22%25%20of%20Vaccinations%20with%20Known%20Race%22,%22sort%22:%22desc%22%7D" rel="nofollow" style="" target="_blank">Kaiser Family Foundation data</a><marked-tail cc-select="true" class="mark-selected" data-anno-uid="anno-uid-9c53kaxa118" style=""> representing race and ethnicity comes from a variety of public sources. Persons of Hispanic origin may be of any race. However, states vary in whether they include or exclude Hispanic individuals in racial categories. Additionally, some states vary in whether they include or exclude Hispanic individuals in racial categories in their reporting of vaccination data. We have a made a note in our table which states do so.</marked-tail></p>
</div></div></div><div data-anno-uid="anno-uid-m2jvjanvttq" id="ad_bnr_btf_01" style="margin-bottom: 80px;"></div><footer class="cnnix__footer" data-anno-uid="anno-uid-qmw3x1a4lyp"><div class="cnnix__footer__contents" data-anno-uid="anno-uid-byonmvh31p8"><div class="row" data-anno-uid="anno-uid-t827uxp2u4"><h2 class="cnnix__footer__title" data-anno-uid="anno-uid-w64q66qtkii"><marked-text class="" data-anno-uid="anno-uid-9nv5669yoki" style="">More of CNN’s Covid-19 coverage</marked-text><ul class="cnnix__footer__related-stories" data-anno-uid="anno-uid-9f685lu8g6r"><li data-anno-uid="anno-uid-votd55m0ov"><a data-anno-uid="anno-uid-6k3nmjzdy08" href="https://www.cnn.com/2020/12/28/health/coronavirus-unknown-facts-intl-hnk-dst/index.html"><h3 class="" data-anno-uid="anno-uid-1t2igt0arj9" style="">What we still don’t know</h3><img alt="" class="" data-anno-uid="anno-uid-qyos07m0il" src="https://cdn.cnn.com/cnnnext/dam/assets/201225172423-20201228-covid-mask-illustration-exlarge-tease.jpg" style=""><p class="" data-anno-uid="anno-uid-p48zrov16" style="">There’s still a lot we don’t know — including where the virus came from and when the pandemic will end.</p></a></li><li data-anno-uid="anno-uid-y8x4e5lm7g"><a data-anno-uid="anno-uid-mcz2tsde8" href="https://www.cnn.com/2021/02/04/health/covid-vaccine-side-effects-wen-wellness/index.html"><h3 class="" data-anno-uid="anno-uid-jmdhwpsvnlg" style="">Preparing for your vaccination</h3><img alt="" class="" data-anno-uid="anno-uid-pdlpkcl6s8" src="https://cdn.cnn.com/cnnnext/dam/assets/210216133506-20210216-covid-vaccine-large-tease.jpg" style=""><p class="" data-anno-uid="anno-uid-c16kof9j9u5" style="">CNN Medical Analyst Dr. Leana Wen shares how to plan for taking care of ourselves and our loved ones as more people get vaccinated.</p></a></li><li data-anno-uid="anno-uid-eth4awp9kl"><a data-anno-uid="anno-uid-4urka7olfoo" href="https://www.cnn.com/2020/07/07/health/how-to-wear-mask-properly-wellness-trnd/index.html"><h3 class="" data-anno-uid="anno-uid-ng2bdm7taq" style="">How to wear masks</h3><img alt="" class="" data-anno-uid="anno-uid-thlh8dohl1q" src="https://cdn.cnn.com/cnnnext/dam/assets/210209132422-20210209-covid-19-live-blog-exlarge-tease.jpg" style=""><p class="" data-anno-uid="anno-uid-hwzmt198wjo" style="">Masks can help protect against the spread of Covid-19, but they’re only effective if you wear them properly.</p></a></li><li data-anno-uid="anno-uid-srtrz39sr89"><a data-anno-uid="anno-uid-bmqz9v1rk2l" href="https://www.cnn.com/coronavirusquestions"><h3 class="" data-anno-uid="anno-uid-l0c1yqklsh">Send us your questions</h3><img alt="" class="" data-anno-uid="anno-uid-tslanijukae" src="https://cdn.cnn.com/cnnnext/dam/assets/200130165125-corona-virus-cdc-image-exlarge-tease.jpg" style=""><p class="" data-anno-uid="anno-uid-hi1zm5tcr3l">CNN is collecting your questions about Covid-19. We’ll be answering some of them in upcoming stories.</p></a></li><li data-anno-uid="anno-uid-8r9x5t0rh2p"><a data-anno-uid="anno-uid-j28v9da26c" href="https://www.cnn.com/audio/podcasts/corona-virus"><h3 class="" data-anno-uid="anno-uid-15c55v4ff02" style="">Listen to our podcast</h3><img alt="" class="" data-anno-uid="anno-uid-293hgs7zdna" src="https://cdn.cnn.com/cnnnext/dam/assets/200301143532-coronavirus-fact-vs-fiction-exlarge-tease.jpg" style=""><p class="" data-anno-uid="anno-uid-2smaoqv5yqw">Join CNN Chief Medical Correspondent Dr. Sanjay Gupta for the latest news about Covid-19.</p></a></li><li data-anno-uid="anno-uid-abvlfxc0scs"><a data-anno-uid="anno-uid-ujc6u57b1eg" href="https://www.cnn.com/specials/coronavirus-newsletter"><h3 class="" data-anno-uid="anno-uid-aey4ucf64p5">Subscribe to our newsletter</h3><img alt="" class="" data-anno-uid="anno-uid-cmj75v128o" src="https://cdn.cnn.com/cnnnext/dam/assets/200311143909-20200311-corona-virus-fact-fiction-exlarge-tease.jpg" style=""><p class="" data-anno-uid="anno-uid-e2mg1f80gul" style="">Get the facts from CNN delivered to your inbox daily.</p></a></li></ul></h2></div><div class="row" data-anno-uid="anno-uid-uaykvd8s1w"><div class="col s12 m5 l7 followLogo" data-anno-uid="anno-uid-7uy6aqycuj8"><a data-anno-uid="anno-uid-n1elf1rlg9" href="https://cnn.com" rel="noopener nofollow noreferrer"><svg data-anno-uid="anno-uid-11lxecczntz" height="50px" version="1.1" viewBox="0 0 50 50" width="50px" xmlns="https://www.w3.org/2000/svg"><rect data-anno-uid="anno-uid-sgj60am8k6" height="50" style="fill:#cc0000;fill-opacity:1;stroke:none;" width="50" x="0" y="0"></rect><path d="M 41.804688 16.015625 L 41.804688 30.648438 C 41.804688 31.257812 41.421875 31.769531 40.851562 31.925781 C 40.75 31.957031 40.632812 31.96875 40.519531 31.96875 C 40.089844 31.96875 39.589844 31.753906 39.238281 31.152344 C 39.21875 31.117188 37.78125 28.644531 35.597656 24.871094 C 34.015625 22.148438 32.382812 19.335938 32.355469 19.285156 C 32.179688 18.988281 31.941406 18.847656 31.710938 18.90625 C 31.566406 18.949219 31.402344 19.085938 31.402344 19.351562 L 31.402344 30.648438 C 31.402344 31.257812 31.015625 31.769531 30.449219 31.925781 C 29.964844 32.054688 29.28125 31.925781 28.828125 31.152344 C 28.808594 31.121094 27.476562 28.816406 25.441406 25.3125 C 23.734375 22.375 21.976562 19.335938 21.945312 19.285156 C 21.769531 18.988281 21.527344 18.84375 21.296875 18.90625 C 21.152344 18.949219 20.984375 19.085938 20.984375 19.351562 L 20.984375 30.402344 C 20.984375 31.160156 20.3125 31.832031 19.550781 31.832031 L 13.941406 31.832031 C 10.175781 31.832031 7.113281 28.769531 7.113281 25.003906 C 7.113281 21.238281 10.175781 18.175781 13.941406 18.175781 L 16.859375 18.175781 L 16.859375 16.015625 L 13.945312 16.015625 C 8.984375 16.015625 4.957031 20.039062 4.957031 25.003906 C 4.957031 29.964844 8.984375 33.988281 13.945312 33.988281 L 19.609375 33.988281 C 21.765625 33.988281 23.148438 32.726562 23.148438 30.402344 L 23.148438 25.273438 C 23.148438 25.273438 26.757812 31.496094 26.925781 31.777344 C 29.222656 35.671875 33.554688 34.058594 33.554688 30.707031 L 33.554688 25.273438 C 33.554688 25.273438 37.167969 31.496094 37.335938 31.777344 C 39.632812 35.671875 43.964844 34.058594 43.964844 30.707031 L 43.964844 16.015625 Z M 41.804688 16.015625 " data-anno-uid="anno-uid-vghp7k07wui" style="stroke:none;fill-rule:nonzero;fill:#ffffff;fill-opacity:1;"></path><path d="M 10.15625 25.003906 C 10.15625 22.898438 11.859375 21.191406 13.964844 21.191406 L 16.859375 21.191406 L 16.859375 19.03125 L 13.945312 19.03125 C 10.652344 19.03125 7.980469 21.710938 7.980469 24.996094 C 7.980469 28.289062 10.660156 30.960938 13.945312 30.960938 L 19.550781 30.960938 C 19.867188 30.960938 20.113281 30.652344 20.113281 30.398438 L 20.113281 19.351562 C 20.113281 18.742188 20.5 18.230469 21.066406 18.074219 C 21.550781 17.945312 22.234375 18.074219 22.6875 18.847656 C 22.707031 18.882812 24.089844 21.257812 26.191406 24.878906 C 27.835938 27.71875 29.542969 30.660156 29.574219 30.714844 C 29.75 31.011719 29.996094 31.15625 30.222656 31.09375 C 30.367188 31.050781 30.539062 30.914062 30.539062 30.648438 L 30.539062 19.351562 C 30.539062 18.742188 30.917969 18.230469 31.484375 18.074219 C 31.96875 17.945312 32.644531 18.078125 33.097656 18.847656 C 33.117188 18.882812 34.335938 20.984375 36.339844 24.4375 C 38.109375 27.496094 39.945312 30.660156 39.980469 30.714844 C 40.15625 31.011719 40.398438 31.15625 40.628906 31.09375 C 40.773438 31.050781 40.941406 30.914062 40.941406 30.648438 L 40.941406 16.015625 L 38.777344 16.015625 L 38.777344 24.726562 C 38.777344 24.726562 35.167969 18.503906 34.996094 18.222656 C 32.703125 14.328125 28.367188 15.941406 28.367188 19.292969 L 28.367188 24.726562 C 28.367188 24.726562 24.757812 18.503906 24.589844 18.222656 C 22.292969 14.328125 17.960938 15.941406 17.960938 19.292969 L 17.960938 28.203125 C 17.960938 28.527344 17.714844 28.8125 17.363281 28.8125 L 13.964844 28.8125 C 11.859375 28.808594 10.15625 27.101562 10.15625 25.003906 Z M 10.15625 25.003906 " data-anno-uid="anno-uid-yvt4fqyqfz" style="stroke:none;fill-rule:nonzero;fill:#ffffff;fill-opacity:1;"></path></svg></a></div><div class="col s12 m3 l2" data-anno-uid="anno-uid-s9f6kx7o2dc"><span class="followText" data-anno-uid="anno-uid-yhkqlnl14v">Follow CNN</span></div><div class="col s12 m4 l3" data-anno-uid="anno-uid-cfo01oc6jrv"><ul class="socialBr" data-anno-uid="anno-uid-e293ymfeji"><li data-anno-uid="anno-uid-673zjg4de3h"><a data-anno-uid="anno-uid-wlggm2oqj6" href="https://facebook.com/cnn" rel="noopener nofollow noreferrer" target="_blank"><svg class="facebook-icon" data-anno-uid="anno-uid-bhce48isi09" fill="#e6e6e6" height="24" viewBox="0 0 64 64" width="24" xmlns="https://www.w3.org/2000/svg"><path d="M56,5.1H8c-1.6,0-3,1.4-3,3v48.8c0,1.7,1.3,3,3,3h25.9V38.7h-7v-8.3h7v-6.1 c0-7.1,4.3-10.9,10.5-10.9c3,0,5.9,0.2,6.7,0.3v7.7h-4.7c-3.4,0-4.1,1.6-4.1,4v5h8.1l-1,8.3h-7v21.2H56c1.6,0,3-1.4,3-3V8.1 C59,6.4,57.7,5.1,56,5.1" data-anno-uid="anno-uid-kocogx3qof"></path></svg></a></li><li data-anno-uid="anno-uid-aroslucm9hu"><a data-anno-uid="anno-uid-cvmslx6up7d" href="https://twitter.com/cnn" rel="noopener nofollow noreferrer" target="_blank"><svg class="twitter-icon" data-anno-uid="anno-uid-lm7ng34v0pi" fill="#e6e6e6" height="24" viewBox="0 0 64 64" width="24" xmlns="https://www.w3.org/2000/svg"><path d="M60,15.2c-2.1,0.9-4.3,1.5-6.6,1.7c2.4-1.4,4.2-3.6,5.1-6.1c-2.2,1.3-4.7,2.2-7.3,2.7 c-2.1-2.2-5.1-3.5-8.4-3.5c-6.3,0-11.5,5-11.5,11.1c0,0.9,0.1,1.7,0.3,2.5C22,23.2,13.6,18.8,7.9,12c-1,1.6-1.6,3.5-1.6,5.6 c0,3.9,2,7.3,5.1,9.2c-1.9-0.1-3.7-0.6-5.2-1.4v0.1c0,5.4,4,9.9,9.2,10.9c-1,0.3-2,0.4-3,0.4c-0.7,0-1.5-0.1-2.2-0.2 c1.5,4.4,5.7,7.6,10.7,7.7c-3.9,3-8.9,4.8-14.3,4.8c-0.9,0-1.8-0.1-2.7-0.2c5.1,3.2,11.1,5,17.6,5c21.1,0,32.7-16.9,32.7-31.6 c0-0.5,0-1,0-1.4C56.5,19.4,58.5,17.4,60,15.2" data-anno-uid="anno-uid-b3jv59gl3ig"></path></svg></a></li><li data-anno-uid="anno-uid-18rpm65fcxti"><a data-anno-uid="anno-uid-76tb7h15aao" href="https://instagram.com/cnn" rel="noopener nofollow noreferrer" target="_blank"><svg class="instagram-icon" data-anno-uid="anno-uid-gmp672bnodd" fill="#e6e6e6" height="24" viewBox="0 0 64 64" width="24" xmlns="https://www.w3.org/2000/svg"><path d="M47,13.2c-1.9,0-3.5,1.6-3.5,3.6s1.6,3.6,3.5,3.6s3.5-1.6,3.5-3.6S49,13.2,47,13.2 L47,13.2z M31.9,23c-5.1,0-9.3,4.3-9.3,9.5s4.2,9.5,9.3,9.5s9.3-4.3,9.3-9.5S37,23,31.9,23L31.9,23z M31.9,46.7 c-7.7,0-14-6.4-14-14.2s6.3-14.2,14-14.2s14,6.4,14,14.2S39.6,46.7,31.9,46.7L31.9,46.7z M15.7,8.8c-3.9,0-7,3.2-7,7.1v33.2 c0,3.9,3.1,7.1,7,7.1h32.7c3.9,0,7-3.2,7-7.1V15.9c0-3.9-3.1-7.1-7-7.1C48.4,8.8,15.7,8.8,15.7,8.8z M48.3,60.9H15.7 C9.2,60.9,4,55.6,4,49.1V15.9C4,9.4,9.2,4.1,15.7,4.1h32.7C54.8,4.1,60,9.4,60,15.9v33.2C60,55.6,54.8,60.9,48.3,60.9L48.3,60.9z" data-anno-uid="anno-uid-q04rdakzk9d"></path></svg></a></li><li data-anno-uid="anno-uid-teva047fdg9"><a data-anno-uid="anno-uid-56wqvdbdqrt" href="https://youtube.com/user/cnn" rel="noopener nofollow noreferrer" target="_blank"><svg class="youtube-icon" data-anno-uid="anno-uid-oxmb4o61er" fill="#e6e6e6" height="24" viewBox="0 0 64 64" width="24" xmlns="https://www.w3.org/2000/svg"><path d="M61.32,17.22A7.66,7.66,0,0,0,56,11.89c-4.77-1.28-24-1.28-24-1.28s-19.15,0-24,1.28a7.66,7.66,0,0,0-5.33,5.33A79.91,79.91,0,0,0,1.4,32,80.28,80.28,0,0,0,2.73,46.78,7.66,7.66,0,0,0,8.06,52.1c4.76,1.29,24,1.29,24,1.29s19.14,0,24-1.29a7.67,7.67,0,0,0,5.32-5.32A80.23,80.23,0,0,0,62.6,32,79.86,79.86,0,0,0,61.32,17.22Zm-35.42,24V22.84l16,9.19Z" data-anno-uid="anno-uid-3nzzuywqr6v"></path></svg></a></li></ul></div></div><div class="row" data-anno-uid="anno-uid-mo0zm9tj1a"><ul class="cnnix__footer__legal__list" data-anno-uid="anno-uid-l5ekeh61qpb"><li class="cnnix__footer__legal__list__item" data-anno-uid="anno-uid-jy3km0vus4q"><a class="cnnix__footer__legal__links" data-anno-uid="anno-uid-fwswkcynlxn" href="https://cnn.com/terms" rel="noopener nofollow noreferrer" target="_blank">Terms of Use</a></li><li class="cnnix__footer__legal__list__item" data-anno-uid="anno-uid-3lka5yscm7q"><a class="cnnix__legal__links" data-anno-uid="anno-uid-68ufbdyyt4" href="https://cnn.com/privacy" rel="noopener nofollow noreferrer" target="_blank">Privacy Policy</a></li><li class="cnnix__footer__legal__list__item" data-anno-uid="anno-uid-spk66gu7cqi"><a class="cnnix__legal__links" data-anno-uid="anno-uid-8062zsan2sj" href="https://cnn.com/accessibility" rel="noopener nofollow noreferrer" target="_blank">Accessibility + CC</a></li><li class="cnnix__footer__legal__list__item" data-anno-uid="anno-uid-wfmvdokamqg"><a class="cnnix__footer__legal__links" data-anno-uid="anno-uid-45kjdu6w0hx" href="https://preferences-mgr.truste.com/?pid=turnermedia01&amp;aid=turnermedia01&amp;type=turner_pop&amp;pid=turnermedia01&amp;aid=turnermedia01" rel="noopener nofollow noreferrer" target="_blank">AdChoices</a></li><li class="cnnix__footer__legal__list__item" data-anno-uid="anno-uid-dq7e44tabvf"><a class="cnnix__legal__links" data-anno-uid="anno-uid-y0215cyh77" href="https://cnn.com/about" rel="noopener nofollow noreferrer" target="_blank">About Us</a></li><li class="cnnix__footer__legal__list__item" data-anno-uid="anno-uid-ik3bs9f9tas"><a class="cnnix__legal__links" data-anno-uid="anno-uid-qxgx28y6mjq" href="https://tours.cnn.com" rel="noopener nofollow noreferrer" target="_blank">CNN Studio Tours</a></li><li class="cnnix__footer__legal__list__item" data-anno-uid="anno-uid-5rgyhd4nogy"><a class="cnnix__legal__links" data-anno-uid="anno-uid-4v9uqt3s6sn" href="https://store.cnn.com" rel="noopener nofollow noreferrer" target="_blank">CNN Store</a></li><li class="cnnix__footer__legal__list__item" data-anno-uid="anno-uid-v03wex7584"><a class="cnnix__legal__links" data-anno-uid="anno-uid-w97t7e4ekw8" href="https://cnn.com/newsletters" rel="noopener nofollow noreferrer" target="_blank">Newsletters</a></li><li class="cnnix__footer__legal__list__item" data-anno-uid="anno-uid-98jwzvtfbya"><a class="cnnix__legal__links" data-anno-uid="anno-uid-b26wmqfek0o" href="https://cnn.com/transcripts" rel="noopener nofollow noreferrer" target="_blank">Transcripts</a></li><li class="cnnix__footer__legal__list__item" data-anno-uid="anno-uid-5ih056mmf8p"><a class="cnnix__legal__links" data-anno-uid="anno-uid-uzh5grenfq8" href="https://collection.cnn.com" rel="noopener nofollow noreferrer" target="_blank">License Footage</a></li><li class="cnnix__footer__legal__list__item" data-anno-uid="anno-uid-qv4eiul6umd"><a class="cnnix__legal__links" data-anno-uid="anno-uid-nh2eeuhd53h" href="https://cnnnewsource.com/" rel="noopener nofollow noreferrer" target="_blank">CNN Newsource</a></li><li class="cnnix__footer__legal__list__item" data-anno-uid="anno-uid-w4o44vd6p0e"><a class="cnnix__legal__links" data-anno-uid="anno-uid-n7inhc16agl" href="https://www.cnn.com/sitemap.html" rel="noopener nofollow noreferrer" target="_blank">Sitemap</a></li></ul></div><div class="row" data-anno-uid="anno-uid-kfr2fjwif8c"><div class="cnnix__footer__copyright" data-anno-uid="anno-uid-ogrqd7pj289"><span class="copyright" data-anno-uid="anno-uid-rdgfv9k1d3o"><marked-text data-anno-uid="anno-uid-o4k4y9b1dz8">© 2021&nbsp;Cable&nbsp;News&nbsp;Network. A </marked-text><a class="m-copyright__links" data-analytics="footer_warnermedia" data-anno-uid="anno-uid-1sxh6tnccfz" href="https://warnermediagroup.com" rel="noopener nofollow noreferrer" style="font-family: 'ATT Aleck Sans', Helvetica, Arial, sans-serif;" title="WarnerMedia"><b data-anno-uid="anno-uid-dhgae6i95zo" style="font-weight: 600 !important;">Warner</b><marked-tail data-anno-uid="anno-uid-n4nppphxclp">Media</marked-tail></a><marked-tail data-anno-uid="anno-uid-zexs7p9rj1"> Company. All&nbsp;Rights&nbsp;Reserved.</marked-tail><br data-anno-uid="anno-uid-if1152ej94c"><marked-tail data-anno-uid="anno-uid-wapzwmjsj7s">CNN&nbsp;Sans ™ &amp; © 2016 Cable&nbsp;News&nbsp;Network.</marked-tail></span></div></div></div></footer><script data-anno-uid="anno-uid-h9sxxjbpk1s" src="../../../2020/health/coronavirus-us-dashboard-assets/app.js?d=1679335408237&amp;v=200323603"></script><iframe data-anno-uid="anno-uid-0bwu4v2ilaer" name="googlefcPresent" style="display: none; width: 0px; height: 0px; border: none; z-index: -1000; left: -1000px; top: -1000px;"></iframe><iframe data-anno-uid="anno-uid-ulfapk3o4l" name="__tcfapiLocator" src="about:blank" style="display: none; width: 0px; height: 0px; border: none; z-index: -1000; left: -1000px; top: -1000px;"></iframe><iframe data-anno-uid="anno-uid-d8n5fduav55" name="googlefcInactive" src="about:blank" style="display: none; width: 0px; height: 0px; border: none; z-index: -1000; left: -1000px; top: -1000px;"></iframe><iframe data-anno-uid="anno-uid-i9nczpob4of" name="googlefcLoaded" src="about:blank" style="display: none; width: 0px; height: 0px; border: none; z-index: -1000; left: -1000px; top: -1000px;"></iframe><script data-anno-uid="anno-uid-icbe5f208n" src="https://lightning.cnn.com/launch/7be62238e4c3/97fa00444124/launch-2878c87af5e3.min.js"></script><script data-anno-uid="anno-uid-9dz0virp53r">_satellite["_runScript1"](function(event, target, Promise) {
window.wminst = window.wminst || {};
wminst.Util = function() {
    return {
        loadCustomVariables: function() {
            this.tmsName = "launch";
            this.businessName = "cnn";
            this.buildVersion = 72; // Build Update Jun 10, 2024
            this.buildEnv = this.getBuildEnv();
            this.buildDate = this.getBuildDate();
            this.debugFlag = "WMINST_DEBUG";
            this.logPrefix = "[WMINST]";
            window.is_expansion = true;
            wminst.subscribersReady = false;
            wminst.hpt_set = 0;
            wminst.buffer_count = 0;
            wminst.is_podcast = 0;
            wminst.is_scrubbed = false;
            if (window.cnn_metadata) {
                window.is_expansion = false;
            }
        },
        getBuildEnv: function() {
            return {
                "development": "dev",
                "staging": "qa",
                "production": "prod"
            }[_satellite.environment.stage];
        },
        getBuildDate: function() {
            return _satellite.buildInfo.buildDate.split("T")[0].replace(/-/g, "");
        },
        getCodeVersion: function() {
            return [this.tmsName, this.businessName, this.buildEnv, this.buildVersion, this.buildDate].join(".");
        },
        setDebug: function(flag) {
            if (flag == true) {
                sessionStorage.setItem(this.debugFlag, true);
            } else {
                sessionStorage.removeItem(this.debugFlag);
            }
        },
        log: function() {
            var logEnabled = sessionStorage.getItem(this.debugFlag);
            if (logEnabled) {
                var args = Array.prototype.slice.call(arguments);
                args.unshift(this.logPrefix);
                console.log.apply(console, args);
            }
        },
        wait: function(ms) {
            const start = Date.now();
            let now = start;
            while (now - start < ms) {
                now = Date.now();
            }
        },
        getTagConsentStatesV1: function(name) {
            return {
                "adobe"             : ["perf-general"],
                "comscore"          : ["perf-vendor"],
                "nielsen"           : ["perf-vendor"],
                "facebook-pixel"    : ["perf-vendor", "social-vendor"],
                "zion"              : ["perf-general", "person-general"],
                "app-nexus-id"      : ["ads-vendor"],
                "trackonomics"      : ["ads-general", "ads-vendor", "behavior-general", "perf-general", "person-general", "social-general", "storage-general"],
                "skimlinks"         : ["ads-vendor"],
                "quantcast"         : ["ads-vendor"],
                "amazon"            : ["ads-vendor"],
                "wunderkind"        : ["iab", "behavior-vendor", "person-vendor", "storage-vendor"],
                "chartbeat"         : ["perf-general"],
                "keywee"            : ["ads-vendor", "behavior-vendor", "storage-vendor", "perf-vendor"],
                "krux"              : ["ads-vendor"],
                "stack-sonar"       : ["ads-general"],
                "optimizely"        : ["behavior-general", "perf-general", "person-general"],
                "bombora"           : ["iab"]
            }[name];
        },
        getTagConsentStatesV2: function(name) {
            return {
                "adobe"             : ["data-store", "content-person-prof", "content-person", "measure-content", "measure-market", "product-develop"],
                "comscore"          : ["vendor", "measure-content"],
                "nielsen"           : ["vendor", "measure-content", "data-store"],
                "facebook-pixel"    : ["data-store", "ads-contextual", "ads-person-prof", "ads-person", "vendor"],
                "zion"              : ["data-store", "ads-person-prof", "ads-person", "content-person-prof", "content-person", "measure-content"],
                "app-nexus-id"      : ["vendor"],
                "trackonomics"      : ["data-store", "measure-ads", "vendor"],
                "hyphensocial"      : ["data-store", "measure-ads", "vendor"],
                "skimlinks"         : ["data-store", "measure-content", "vendor"],
                "amazon"            : ["data-store", "ads-contextual", "ads-person-prof", "ads-person", "vendor"],
                "quantcast"         : ["iab", "data-share", "data-sell", "data-store", "ads-contextual", "ads-person-prof", "ads-person", "measure-content", "measure-market", "product-develop"],
                "wunderkind"        : ["iab", "data-share", "data-sell", "data-store", "ads-contextual", "ads-person-prof", "ads-person", "measure-ads", "measure-market", "product-develop"],
                "chartbeat"         : ["data-store", "measure-content"],
                "keywee"            : ["data-store", "ads-person-prof", "ads-person", "measure-ads", "measure-market", "vendor"],
                "krux"              : ["data-store", "ads-person-prof", "ads-person", "measure-ads", "measure-content", "measure-market"],
                "stack-sonar"       : ["data-store", "ads-contextual", "ads-person-prof", "ads-person"],
                "optimizely"        : ["data-store", "content-person-prof", "content-person", "measure-ads", "measure-content", "vendor"],
                "bombora"           : ["vendor", "data-store", "ads-person-prof", "measure-ads", "measure-content", "product-develop"],
                "outbrain-pixel"    : ["ads-person-prof", "ads-person", "measure-ads"],
                "full-story"        : ["measure-content", "product-develop"],
                "iSpot-pixel"       : ["data-store", "measure-ads", "measure-content", "measure-market", "vendor"]
            }[name];
        },
        getTagConsentStates: function(name) {
            if (window.WM && WM.UserConsent && WM.UserConsent.getVersion().indexOf("1") === 0) {
                return this.getTagConsentStatesV1(name);
            }
            return this.getTagConsentStatesV2(name);
        },
        isUSRegion: function() {
            if (window.WM && WM.UserConsent) {
                return WM.UserConsent.getGeoCountry() === "US";
            } else {
                return _satellite.cookie.get("countryCode") === "US";
            }
        },
        usePrismGeoCheck: function() {
            return !_satellite.cookie.get("countryCode") && this.isCNNStorePage();
        },
        isTagConsented: function(name) {
            // Special handling for AppNexus ID, and Quantcast
            if (name == "app-nexus-id" && !this.isUSRegion()) {
                return false;
            }
            if (name == "quantcast" && this.isUSRegion()) {
                return false;
            }            
            var states = this.getTagConsentStates(name);
            if (window.WM && WM.UserConsent) {
                if (WM.UserConsent.isReady() && WM.UserConsent.inUserConsentState(states, {id: name})) {
                    return true;
                }
            } else {
                return true;
            }
            return false;
        },
        isPrismEnabled: function() {
            if (window.WM && window.WM.CDP && typeof window.WM.CDP.isIdentityEnabled === "function") {
                return window.WM.CDP.isIdentityEnabled();
            }
            return false;
        },      
        inIFrame: function() {
            try {
                return window.self !== window.top;
            } catch (e) {
            return true;
            }
        },
        getQueryParam: function(key, loc) {
            if (!this.params || loc) {
            var search = loc || window.location.search;
            var params = search.replace(/^\?/, ""), paramObj = {};
            params = params.split("&");
            for (var i = 0; i < params.length; i++) {
              var t = params[i].split("=");
              paramObj[t[0]] = t[1]
            }
            if (!loc) {
                this.params = paramObj;
            } else {
              return paramObj[key] || "";
            }
          }
          return this.params[key] || "";
        },
        getDataLayerV0: function() {
            return (((window.cnn_metadata || {}).business || {}).cnn || {}).page || {};
        },
        getDataLayerV1: function() {
            return (window.CNN || {}).omniture || {};
        },
        getDataLayerV2: function() {
            return (window.CNN || {}).contentModel || {};
        },
        getSectionValue: function(i) {
            return (this.getDataLayerV1().section || {})[i];
        },
        getDL2PageTop: function(i) {
            return (this.getDataLayerV2().analytics || {}).pageTop || {};
        },
        getDL2Prop: function(key) {
            return this.getDataLayerV2()[key] || "";
        },
        commentsEnabled: function() {
            var flag = this.getDataLayerV2().commentsEnabled;
            return flag === "true" || flag === true;
        },
        adsSuppressed: function() {
            return window.CNN?.ads?.showAds === false;
        },
        isSearchPage: function() {
            return window.location.pathname.indexOf("/search") === 0;
        },
        isRefreshPage: function() {
            return wminst.Util.getQueryParam("refresh");
        },
        isHomepage: function() {
            var dataLayer = this.getDataLayerV2();
            return (dataLayer.sectionName || dataLayer.section) === "homepage";
        },
        isTVEPage: function() {
            var dataLayer = this.getDataLayerV2();
            return dataLayer.pageType === "tve" || dataLayer.section === "tv";
        },
        isNGTVPage: function() {
            var dataLayer = this.getDataLayerV1();
            return (dataLayer.friendly_name || "").toLowerCase() === "ngtv";
        },
        isStellarPage: function() {
            return this.getCNNTechStack() === "stellar2.0";
        },
        isUnderscoredPage: function() {
            return this.getSectionValue(0) === "cnn-underscored";
        },
        isStylePage: function() {
            return this.getSectionValue(0) === "style";
        },
        isTravelPage: function() {
            return this.getSectionValue(0) === "travel";
        },
        isFactsFirstPage: function() {
            return this.getSectionValue(1) === "facts first";
        },
        isOnboardingPage: function() {
            return this.getSectionValue(1) === "onboarding";
        },
        isSponsoredArticlePage: function() {
            return this.getCNNTemplateType() === "article_sponsor";
        },
        isElectionDynamicPage: function() {
            return window.location.pathname.match(/\/election\//) !== null && window.location.pathname.match(/20(17|18|19)/) !== null;
        },
        isUserAccountPage: function() {
            return window.location.pathname.match('/account/(register|preferences|confirm|reset-password|log-in|payment|onboarding)/?.*') !== null;
        },
        isSignupPage: function() {
            return window.location.pathname.match(/\/signup\/?$/) !== null;
        },
        isNewsletterHub: function() {
            return window.location.pathname.match(/^\/newsletters(\/.*)?$/) !== null;
        },
        isUnderscoredZionPage: function() {
            return window.location.pathname.match(/\/(pets\/editors-favorite-pet-products|home\/women-owned-businesses|fashion\/best-spring-dresses|reviews\/best-linen-sheets|reviews\/best-pillows)\/?$/) !== null;
        },
        isLiveStoryPage: function() {
            return window.location.pathname.indexOf("live-news") !== -1;
        },
        isLiveStoryStellarPage: function() {
            return this.isLiveStoryPage() && this.isStellarPage();
        },      
        isLiveStoryNonStellarPage: function() {
            return this.isLiveStoryPage() && !this.isStellarPage();
        },
        isCNNPlusPage: function() {
            return window.location.hostname.indexOf("plus") !== -1;
        },
        isCNNStorePage: function() {
            return window.location.hostname.indexOf("store") !== -1;
        },
        isCNNIntlPage: function() {
            return window.location.hostname.indexOf("edition") !== -1;
        },
        isSpeedyPage: function() {
            return window.location.hostname.indexOf("-m.cnn.com") !== -1;
        },
        isDynamicPage: function() {
            return this.isSearchPage() || this.isRefreshPage() || this.isElectionDynamicPage() || this.isLiveStoryNonStellarPage() || this.isSpeedyPage() || this.isOnboardingPage();
        },
        isLightweightPage: function() {
            return this.isUserAccountPage() || this.isNewsletterHub();
        },
        isFavePage: function() {
            var hostName = window.location.hostname;           
            return hostName.indexOf("fave.api.cnn.io") !== -1 || hostName.indexOf("fave-api.cnn.com") !== -1;
        },
        isPoliticsExplorer: function() {
            var dataLayer = this.getDataLayerV1();
            return dataLayer.is_explorer === true || dataLayer.is_explorer === "true";
        },
        isFBIAPage: function () {
            var dataLayer = this.getDataLayerV1();
            return dataLayer.fbia === true || dataLayer.fbia === "true";
        },
        isLiveStoryTemplateType: function() {
            var dataLayer = this.getDataLayerV1();
            return dataLayer.template_type == "live story" || dataLayer.template_type === "article_livestory";
        },
        isEmpty: function(obj) {
            for (var key in obj) {
                if (obj.hasOwnProperty(key))
                    return false;
            }
            return true;
        },
        reverse: function(obj) {
            const ret = {};
            Object.keys(obj).forEach(key => {
                ret[obj[key]] = key;
            });
            return ret;
        },
        isHexString: function(str) {
            const regexExp = /^[A-Fa-f0-9]+$/;
            return regexExp.test(str);
        },
        sendImagePixel: function(url) {
            var image = new Image();
            image.src = url;
            image.style.display = "none";
            image.width = 1;
            image.height = 1;
        },
        loadScript: function(src, callback) {
            var e = document.createElement('script');
            e.type = 'text/javascript';
            e.async = true;
            e.src = src;
            if (callback) {
                e.addEventListener('load', callback);
            }
            var n = document.getElementsByTagName('script')[0];
            n.parentNode.insertBefore(e, n);
        },
        getCookie: function(name, flag) {
            var r = _satellite.cookie.get(name)|| "";
            if (flag === 'c' || flag === 1) {
                _satellite.cookie.set(name, "-", -1000);
            }
            return unescape(r);
        },
        setCookie: function(name, value) {
            _satellite.cookie.set(name, value, { domain: ".cnn.com" });
        },
        removeCookie: function(name) {
            // if cookie is not removed on first attempt, try again with a different method
            _satellite.cookie.remove(name);
            if (_satellite.cookie.get(name)) {
                document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=.cnn.com;";
            }
        },
        getCookieWithDomain: function(name) {
            const domain = window.location.hostname.replace('www.', '');
            const subdomain = domain.substr(0, domain.indexOf('.'));
            let host = '';
            if (!['cnn', 'us', 'edition', 'arabic', 'cnnespanol'].includes(subdomain)) {
                host = "_" + (subdomain || domain);
            }
            return this.getCookie(name + host);
        },
        base64Decode: function(str) {
            var rval;
            try {
                rval = window.atob(str);
            } catch (e) {}
            return rval;
        },
        getBusinessUnit: function() {
            return this.getSiteSpecificSettings(1);
        },
        addBrandingEvent: function() {
            var bcp = this.getCNNBrandingPartner();
            if (!["", "nvs", "no value set", "no-value-set"].includes(bcp)) {
               s.events = "event21," + s.events;
            }
        },
        addArticleEvent: function() {
            var tt = this.getDataLayerV1().template_type || "";
            var cctype = this.getDataLayerV1().cap_content_type || "";
            if (tt == "article" || cctype == "article"){
                s.events += ",event39";
            }
        },
        addCommentsEvent: function() {
            if (this.commentsEnabled()) {
               s.events += ",event118";
            }
        },
        setPageEvents: function() {
            s.events = "event26";
            this.addBrandingEvent();
            this.addArticleEvent();
            var tt = this.getDataLayerV1().template_type || "";
            if (tt !== "error") {
                var pathName = window.location.pathname;
                if (pathName.includes("/account/register")) {
                    s.events += ",event51";
                }
                if (pathName.split("/")[1] == "video-day") {
                    s.events += ",event63";
                }
            }
            this.addCommentsEvent();
            s.linkTrackEvents = s.events;
        },
        getCNNBusinessName: function() {
            return "cnn";
        },
        getCNNCampaign: function(){
           if (wminst.Util.isFBIAPage()) {
               return "fbia";
           }
           return;
        },
        getCNNDomainName: function() {
          var hostname = window.location.hostname.toLowerCase();
          hostname = hostname.replace("www.","");
          return hostname;
        },
        getCNNPageURL: function() { //s.pageURL or g variable
            var rval = window.location.href.toLowerCase(), loc = "";
            if (wminst.Util.isFBIAPage()) {
                loc = rval;
                rval = "";
                if (loc.indexOf("ofs=fbia") > -1) {
                    loc = loc.replace("ofs=fbia", "csr=fbiacnn"); //suppressing string which is not expected as per new requirement
                }
                var jj = (loc.indexOf("?") != -1 ? "&" : "?");
                if (loc.indexOf("csr=fbiacnn") > -1) {
                    rval = loc + "";
                } else {
                    rval = loc + jj + "csr=fbiacnn"; // added expected substring
                }
            }
            return rval;
        },
        getCNNPageType: function() {
            var rval = "";
            try {
                var title = document.title.toLowerCase();
                if (title.indexOf("page not found") !== -1 || wminst.Util.getCNNTemplateType().includes("error") || title == "error") {
                    rval = "errorPage";
                }
            } catch (err) {}
            return rval;
        },
        getCNNAuthor: function() { //prop2,eVar2 - business.cnn.page.author
            var rval = "";
            if (window.is_expansion) {
                try {
                    rval = window.cnn_d.omniture.cap_author;
                } catch (e) {}
                try {
                    rval = window.CNN.omniture.cap_author.toString();
                } catch (e) {}
            } else {
                try {
                    rval = window.cnn_metadata.business.cnn.page.author;
                } catch (e) {}
                if (!rval) {
                    if (document.getElementsByName("AUTHOR").item(0)) {
                        rval = document.getElementsByName("AUTHOR").item(0).content;
                    } else if (document.getElementsByName("author").item(0)) {
                        rval = document.getElementsByName("author").item(0).content;
                    }
                }
            }
            if (typeof rval === "undefined" || rval == "no-value-set" || rval == "nvs") rval = "";
            return rval.toLowerCase();
        },
        getPageAttribution: function() { //prop4,eVar4 - page HPlocation
            var rval = "";
            var ishptCookie = false;
            var hptcookie = wminst.Util.getCookie("hpt");
            var linkTrackingCookie = wminst.Util.getCookie("linkTracking");
            this.log("getPageAttribution hptcookie =", hptcookie, "linkTrackingCookie =", linkTrackingCookie);
            var regex = new RegExp("^[A-Za-z0-9=]+$");
            if ((typeof linkTrackingCookie == 'undefined' || linkTrackingCookie == "") && typeof hptcookie !== 'undefined') {
                ishptCookie = true;
            }
            var attributionCookie = linkTrackingCookie || hptcookie;
            if ((typeof attributionCookie != "undefined" && attributionCookie != "" && attributionCookie.indexOf("breaking:") != -1) || !regex.test(attributionCookie)) {
                rval = attributionCookie;
            } else if (document.referrer.indexOf("cnn.com") !== -1) {
                rval = wminst.Util.getQueryParam("linkTracking") || wminst.Util.getQueryParam("hpt");
                try {
                    rval = rval.replace(/no\-value\-set/g, "");
                } catch (e) {}
                var prev_rval = rval;
                try {
                    if (attributionCookie) {
                        rval = attributionCookie;
                        if (attributionCookie.indexOf("_") === -1 && attributionCookie.indexOf("|") === -1 && typeof this.base64Decode(attributionCookie) !== 'undefined') {
                            rval = this.base64Decode(attributionCookie);
                        }
                    }
                } catch (e) {}
                if (rval) {
                    wminst.hpt_set = 1;
                } else {
                    rval = prev_rval;
                }
            }
            if (window.is_expansion != 0) {
                if (wminst.Util.getQueryParam("cnnapp") && wminst.Util.getQueryParam("cnnapp") != null) {
                    rval = "cnnapp:" + wminst.Util.getQueryParam("cnnapp");
                }
                if (wminst.Util.getQueryParam("eref") && wminst.Util.getQueryParam("eref") != null) {
                    rval = "eref:" + wminst.Util.getQueryParam("eref");
                }
                if (wminst.Util.getQueryParam("iref") && wminst.Util.getQueryParam("iref") != null) {
                    rval = "iref:" + wminst.Util.getQueryParam("iref");
                }
                if (wminst.Util.getQueryParam("refresh") && wminst.Util.getQueryParam("refresh") != null) {
                    rval = "auto-refresh";
                }
            }
            if(rval !== "") {
              rval = rval.replace(/no-value-set/g, "nvs");
              rval = rval.toLowerCase();   
            }
            this.removeCookie(ishptCookie ? "hpt" : "linkTracking");
            return rval;
        },
        setPageAttribution: function() {
            s.eVar105 = this.getPageAttribution();
        },
        getPhotoGalleryName: function(){ //prop6,eVar6 - Photo Gallery name
            var dataLayer = this.getDataLayerV1();
            return (dataLayer.gallery_name || "").toLowerCase();
        },
        getCNNVisitNumber: function(rollday) { //prop8,eVar8 - visit_number.$30Day  
            rollday = rollday || 28; //default rolling day is 28
            var todaydate = new Date().getTime();
            if (typeof(Storage) !== "undefined") { //check for web storage support
                if (localStorage.startdate) { //check for start date
                    if (sessionStorage.online) { //check for session variable
                        var daysinceonline = Math.ceil((todaydate - sessionStorage.online) / 86400000);
                        if (daysinceonline > 1) { //if session is older than 24 hours, reset session start time and count as a visit
                            localStorage.visittype = "repeat"; //set visit type (new vs repeat)
                            localStorage.visitnum = Number(localStorage.visitnum) + 1; //increment visit number
                            sessionStorage.online = todaydate; //set session variable
                        }
                    } else { //new session
                        localStorage.visittype = "repeat"; //set visit type (new vs repeat)
                        localStorage.visitnum = Number(localStorage.visitnum) + 1; //increment visit number
                        sessionStorage.online = todaydate; //set session variable
                    }
                    var daysincestart = Math.ceil((todaydate - localStorage.startdate) / 86400000);
                    if (daysincestart > Number(rollday)) { //if days since start date is greater than rolling day, set new start date
                        localStorage.startdate = todaydate;
                        localStorage.visittype = "new";
                        localStorage.visitnum = 1;
                    }
                } else { //first new visit
                    localStorage.startdate = todaydate; //set new start date
                    localStorage.visittype = "new"; //set visit type (new vs repeat)
                    localStorage.visitnum = 1; //set visit number
                    sessionStorage.online = todaydate; //set session variable
                }
                return localStorage.visittype + ":" + localStorage.visitnum;
            } else {
                return "new:1";
            }
        },
        getCNNPublishDate: function() {
            var dataLayer = this.getDataLayerV1();
            rval = dataLayer.publish_date || "";
            if (dataLayer.last_updated_date) {
                rval += "|" + dataLayer.last_updated_date;
            }
            if (!rval) {
                rval = window.cnn_d?.omniture?.publish_date;
            }
            return rval;
        },
        populatePublishDate: function(){
            var rval = wminst.Util.getCNNPublishDate();
            var etype = ["content","live story","article_livestory","gallery"];
            var rttype = wminst.Util.getCNNTemplateType("long");
            var result = false;
            if (typeof rttype !== 'undefined') {
               for(var i in etype){
                  if(rttype.indexOf(etype[i]) != -1){
                      result  = true;
                  }
                }
            }
           if (result) {
              return rval;
           } else {
              return "";
           }
        },
        getCNNDaysSinceLastPublish: function(d) { //prop10,eVar10 - days_since_publish
            var e = new Date();
            var p;
            var j;
            if (d == 'a') {
                try {
                    d = window.cnn_metadata.business.cnn.page.publish_date;
                } catch (err) {}
                try {
                    d = window.CNN.omniture.publish_date || d;
                } catch (err) {}
                j = new Date(d);
            } else if (d.toString().indexOf("/") != -1) {
                p = d.split("/");
                if (p[0].length != 4) {
                    p[2] = "20" + p[2];
                    j = new Date(p[2] + "/" + p[0] + "/" + p[1]);
                } else {
                    j = new Date(d);
                }
            } else {
                j = new Date(d);
            }
            var ONE_DAY = 1000 * 60 * 60 * 24;
            var date1_ms = e.getTime();
            var date2_ms = j.getTime();
            var difference_ms = Math.abs(date1_ms - date2_ms)
            var days = Math.round((difference_ms / ONE_DAY))
            if (isNaN(days)) {
                return "";
            }
            if (window.is_expansion != 0) {
                return Math.round((difference_ms / ONE_DAY)).toString()
            } else if (window.is_expansion == 0 && typeof window.cnn_metadata.days_since_publish !== "undefined") {
                try {
                    return window.cnn_metadata.days_since_publish;
                } catch (err) {}
            }
        },
        populateDaysSinceLastPublish: function(){
            var rval =  wminst.Util.getCNNDaysSinceLastPublish("a");
            var etype = ["content:","live story","article_livestory"];
            var rttype = wminst.Util.getCNNTemplateType("long");
            var result = false;
            if (typeof rttype !== 'undefined') {
                for(var i in etype){
                    if (rttype.indexOf(etype[i]) != -1){
                        result  = true;
                    }
                }
            }
            if(result) {
                return rval;
            } else {
                return "";
            }
        },
        getCNNBrandingPartner: function() { //prop11,eVar11 - page branding content partner
            var dataLayer1 = this.getDataLayerV1();
            var dataLayer2 = this.getDataLayerV2();
            var rval = (dataLayer2.branding || {}).key || dataLayer1.branding_content_page || "";
            return rval.toLowerCase();
        },
        getCNNCapContentType: function (){ //prop13,eVar13 - cap_content_type
            var dataLayer1 = this.getDataLayerV1();
            var dl2PageTop = this.getDL2PageTop();
            var rval = dataLayer1.cap_content_type || "";
            if (dl2PageTop.type === "gallery") {
                rval = "gallery";
            }
            return rval.toLowerCase();
        },
        getCNNCapGenre: function (){ //prop5,eVar5 - cap genre
            var dataLayer = this.getDataLayerV1();
            return (dataLayer.cap_genre || "nvs").toLowerCase().replace("no-value-set", "nvs");
        },
        getCNNCapMediaType: function() {
            var dataLayer = this.getDataLayerV1();
            return (dataLayer.cap_media_type || "nvs").toLowerCase().replace("no-value-set", "nvs");
        },
        getCNNBrandingSocial: function() { //prop14,eVar14 - Branding Social
            var rval = "";
            try {
                if (window.CNN && window.CNN.omniture) {
                    if (window.CNN.omniture.fbia === true) {
                        rval = window.CNN.omniture.branding_social;
                    }
                }
            } catch(err) {}
            try {
                if (window.navigator.userAgent && window.navigator.userAgent == "cnn-mobile-app") {
                    return window.navigator.userAgent;
                }
            } catch(err){}
            var hostName = window.location.hostname;
            if (hostName.indexOf("fave.api.cnn.io") != -1 || hostName.indexOf("fave-api.cnn.com") != -1) {
                var pathName = window.location.pathname;
                if (pathName.indexOf("/v1/amp") != -1) {
                    rval = "google amp"; //google amp
                }
                if (pathName.indexOf("/v1/fav") != -1) {
                    rval = "embed"; //embed
                }
            }
            rval = rval.toLowerCase();
            return rval;
        },
        getCNNTrafficPartner: function() { // eVar15 - Traffic Partner
           var rval = "";
           try {
             rval = _satellite.cookie.get("FastAB");
           } catch(err) {}
           return rval;
        },
        getIreportgetMember: function() { //prop17,eVar17 - ireport member
            var irptMember = wminst.Util.getCNNAuthenticated("authid", "displayname", "member", "anonymous", "NonMember", "?");
            if (window.location.host.indexOf("politics") == -1 && window.is_expansion != 0) {
                return irptMember;
            } else {
                return null;
            }
        },
        getCNNPageImpression: function() { //prop18,eVar18 - page impressions
            var rval = window.cnnPSproducts || "";
            var hptcookie = wminst.Util.getCookie("hpt2");
            if (document.referrer.indexOf("cnn.com") > -1) {
                try {
                    if (hptcookie) {
                        rval = hptcookie;
                        if (hptcookie.indexOf("_") == -1) {
                            rval = this.base64Decode(hptcookie);
                        }
                    }
                } catch(e) {}
                //document.cookie = "hpt2=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;";
            } else {
                if (hptcookie) {
                    document.cookie = "hpt2=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=.cnn.com;";
                }
            }
            rval = rval.replace(/no-value-set/g, "nvs");
            rval = rval.toLowerCase();
            return rval;
        },
        getCNNVideoOpportunity: function() { //eVar22 - video embed count
          var rval = "0";
          var ttype = "";
          try { rval = window.cnn_metadata.business.cnn.page.video_embed_count; } catch(e) {}
          try { rval = window.CNN.omniture.video_opportunity || "0"; } catch(e) {}
          ttype = wminst.Util.getCNNTemplateType();
          if (typeof ttype !== 'undefined' && ttype.indexOf("index") > -1) {
            rval = "";
          }
          return rval;
        },
        getCNNPageHeadline: function() { //prop23,eVar23 - page headline
            var rval = "nvs", tt = "";
            try {   
                rval = window.CNN.omniture.headline;
                tt   = window.CNN.omniture.template_type;
            } catch(e) {}
            try {   
                if(typeof window.cnn_d != "undefined" && typeof window.cnn_d.omniture != "undefined" && window.cnn_d.omniture.headline != "undefined"){
                rval = window.cnn_d.omniture.headline;
                tt   = window.cnn_d.omniture.template_type;
                }
            } catch(e) {}
            try {
                if(rval == "no-value-set" || tt == "specials" || tt == "section front" || tt == "index") {return null;}
                rval = rval.toLowerCase();
            } catch(e) {rval = "";}
            return rval;
        },
        getCNNPageName: function(pathname) { //pageName,eVar26 - page.name
            var rval = pathname || window.location.pathname;
            rval = rval.toLowerCase();
            rval = rval.replace(/^.*\/\/[^\/]+/, "");           //remove domain
            rval = rval.replace(/\/index(.html)?(\/)?$/, "");   //remove /index/ and /index.html/
            rval = rval.replace(/h_[a-z0-9]+\/?$/, "");         //remove last folder ID
            rval = rval.replace(/\/?$/, "/");                   //add trailing slash
            if (rval === "/") rval += "homepage";
            return rval;
        },
        getCNNBaseURL: function() { //prop26 - Base URL
            var hostname = window.location.hostname;
            var pathname = window.location.pathname;
            pathname = pathname.replace(/([^\/]+\.[^\/]+$)/,"");
            return hostname + pathname;
        },
        getCNNSection: function(position) { //channel/eVar27, prop28/eVar28
            var rval = "";
            try {
                if (window.is_expansion) {
                    for (var i = 0; i <= position; i++) {
                        if (i > 0) {
                            rval += ":";
                        }
                        try {
                            var s1 = window.CNN.omniture.section[i];
                            if ((s1.indexOf(":")) && (s1.indexOf("electoral college map") > -1)) {
                                var c1 = s1.split(':');
                                rval += c1[0];
                                return rval;
                            }
                        } catch (e) {}
                        if (typeof window.CNN != 'undefined' && typeof window.CNN.omniture != 'undefined') {
                            if (i == 1 && !window.CNN.omniture.section[1]) { //add default value "no value set" for subsection (prop28/eVar28)
                                window.CNN.omniture.section[1] = "no value set";
                                try {
                                    if (this.isNGTVPage()) {
                                        window.CNN.omniture.section[1] = "";
                                    }
                                } catch (e) {}
                            }
                        }
                        if (window.cnn_d && window.cnn_d.omniture && window.cnn_d.omniture.section[i]) {
                            try {
                                rval += window.cnn_d.omniture.section[i] || "";
                            } catch (e) {}
                        } else {
                            try {
                                rval += window.CNN.omniture.section[i] || "";
                            } catch (e) {}
                        }
                    }
                    try {
                        if (typeof window.CNN.omniture !== 'undefined' && window.CNN.omniture.template_type == "list" && position == 0 && rval == "") { //use first path of URL for list pages
                            rval = wminst.Util.getADBPURL("path", 1);
                        }
                    } catch (e) {}
                } else {
                    window.cnn_metadata.section = (typeof window.cnn_metadata.section != "string" ? window.cnn_metadata.section : window.JSON.parse(window.cnn_metadata.section));
                    rval = (window.cnn_metadata.section[position] ? window.cnn_metadata.section[position] : "");
                }
            } catch (e) {}
            return rval;
        },
        getCNNPageFranchise: function() { //prop31,eVar31 - page_franchise
            var rval = "";
            try { rval = cnn_metadata.business.cnn.page.broadcast_franchise || rval; } catch(e) {}
            try { rval = CNN.omniture.cap_show_name || rval; } catch(e) {}
            rval = rval.toLowerCase();
            return rval;
        },
        getCNNLeadingMedia: function() { //eVar111 - leading media
            var dataLayer = this.getDataLayerV2();
            var rval = dataLayer.leadingMediaType || "no media";
            if (rval == "video") {
                rval += "|";
                rval += dataLayer.isVideoCollection ? "collection" : "nocollection"
            }
            return rval;
        },
        getTemplateTypeLookup: function() {
            return {
                b: "blog",
                g: "game",
                it: "interactive",
                c: "content",
                in: "index",
                err: "error",
                e: "ecom",
                s: "signup",
                v: "video",
                sf: "section front",
                sr: "search results",
                fm: "forum",
                o: "other",
                ir: "ireport",
                sp: "specials",
                pm: "perfect market",
                bf: "blog front",
                bc: "blog category",
                t: "topic",
                w: "weather",
                el: "election"
            };
        },
        getCNNTemplateType: function(lookupType) { //prop32,eVar32 - page template_type
            var rval = "";
            if (window.is_expansion) {
                var hostName = window.location.hostname;
                var dataLayer1 = this.getDataLayerV1();
                var dataLayer2 = this.getDataLayerV2();
                var dl2PageTop = this.getDL2PageTop();
                if (["fave.api.cnn.io", "fave-api.cnn.com"].includes(hostName)) {
                    rval = "content";
                } else if (dataLayer1.template_type == 'article') {
                    try {
                        if (dl2PageTop.type === 'gallery' || dataLayer1.cap_content_type === 'gallery') {
                            rval = "content: gallery";
                        } else if (dl2PageTop.type === 'video' || dl2PageTop.type === 'video360') {
                            if (dataLayer2.analytics.isArticleVideoCollection) {
                                rval = "content:video:collection";
                            } else {
                                rval = "content:video:nocollection";
                            }
                        } else {
                            if (dataLayer1.cap_media_type === 'Video') {
                                rval = "content:video";
                            } else {
                                rval = "content: no media";
                            }
                        }   
                    } catch (e) {}
                } else {
                    rval = dataLayer1.template_type;
                }
            } else {
                var dataLayer = this.getDataLayerV1() || window.cnn_metadata || window.cnn_d?.omniture || {};
                var templateTypeCode = dataLayer.template_type;
                rval = ["o", "other"];
                var lookup = this.getTemplateTypeLookup();
                var lookupRev = this.reverse(lookup);
                if (lookup[templateTypeCode] != null) {
                    rval = [templateTypeCode, lookup[templateTypeCode]];
                }
                if (lookupRev[templateTypeCode] != null) {
                    rval = [lookupRev[templateTypeCode], templateTypeCode];
                }
                if (lookupType == "short") {
                    rval = rval[0];
                }
                if (lookupType == "long") {
                    rval = rval[1];
                }
            }
            if (typeof rval == "string") {
                rval = rval.toLowerCase();
            }
            return rval;
        },
        getCNNContentType: function(defaultVal) { //prop33,eVar33 - content_type
            var omnitureRef = (window.cnn_d && window.cnn_d.omniture) || (window.CNN && window.CNN.omniture);
            if (typeof omnitureRef === 'undefined') {
                return defaultVal;
            }

            var tt = "",
                ct = "";
            if (typeof window.cnn_d != 'undefined' && typeof window.cnn_d.omniture != 'undefined' && typeof window.cnn_d.omniture.template_type != 'undefined') {
                tt = window.cnn_d.omniture.template_type;
                ct = "adbp:" + window.cnn_d.omniture.content_type;

            } else {
                if (typeof window.CNN.omniture !== "undefined" && typeof window.CNN.omniture.content_type !== "undefined" && window.CNN.omniture.content_type){
                    ct = window.CNN.omniture.content_type;
                } else {
                    ct = "adbp:none";
                }
                if (typeof ct !== 'undefined' && (ct == "none" || ct == "")) {
                    ct = "adbp:none";
                }
                tt = window.CNN.omniture && window.CNN.omniture.template_type;
            }
            var l = {
                "adbp:blog": ["blog.read", "adbp:blog read"],
                "adbp:content": ["article.read", "adbp:article read"],
                "adbp:game": ["game.play", "adbp:game played"],
                "other:ireport": ["other.ireport", "other:ireport"],
                "other:photo wall": ["content.interactive", "other:photo wall"]
            } [tt];
            var m = {
                "adbp:article read": "article.read"
            } [ct];
            if (m !== null) {
                if (typeof ct !== 'undefined' && ct.indexOf("pivit") !== -1) {
                    return tt + ":" + ct;
                } else {
                    return ct;
                }
            }
            if (!l) {
                return defaultVal;
            }
            return l[1];
        },
        getCNNAuthenticated: function(c1, c2, truevalue, falsevalue, neutralvalue, flag) { //prop34,eVar34 - user authenticated
            var rValue = 0;
            if (wminst.Util.getCookie(c1, flag)) {
                rValue++;
            }
            if (wminst.Util.getCookie(c2, flag)) {
                rValue++;
            }
            if (rValue == 0) {
                return falsevalue;
            } else if (rValue == 1) {
                return neutralvalue;
            } else {
                return truevalue;
            }
        },
        getCNNKruxID: function() { // eVar36 - KruxID
            var rval = "";
            try {
                rval = localStorage.kxkuid;
            } catch (err) {}
            return rval;
        },
        getCNNPlatform: function() { //prop37,eVar37 - page platform
            var rval = "";
            if (navigator.userAgent.match(/iPhone/i)) {
                rval = "smartphone";
            } else if (navigator.userAgent.match(/iPad/i)) {
                rval = "tablet";
            } else if (navigator.userAgent.match(/android/i)) {
                if (navigator.userAgent.match(/mobile/i)) {
                    rval = "smartphone";
                } else {
                    rval = "tablet";
                }
            } else {
                rval = "desktop";
            }
            return rval ? rval : "no value set";
        },
        getCNNSearchInternalKeyword: function() { //prop39,eVar39 - search internal keyword
            var rval = "";
            try {
                rval = wminst.Util.getQueryParam("query");
            } catch(e){}
            return rval;
        },
        getLSPostPosition: function() { //eVar45 - Post Position
            var rval = "";
            try {
                if (this.isLiveStoryTemplateType()) {
                    var post_position = window.CNN.omniture.post_position ? window.CNN.omniture.post_position : 1;
                    var total_post = window.CNN.omniture.total_post ? window.CNN.omniture.total_post : 0;
                    rval = post_position + ":" + total_post;
                }   
            } catch(e) {}
            return rval;
        },
        getCNNPostID: function() { //prop43 - Post ID
            var rval = null;
            var pathName = window.location.pathname;
            if(window.CNN && window.CNN.omniture &&  typeof window.CNN.omniture.post_id != 'undefined' && window.CNN.omniture.post_id != "") {
                rval = window.CNN.omniture.post_id;
            } else {
                 try{
                    pathName = pathName.replace(/\/$/, "");
                    var path_array = pathName.split("/");
                    rval = path_array[path_array.length - 1];
                    if(rval.match(/(^h_)[a-z0-9]+$/) === null){
                        rval = null;
                    }
                } catch(e) {}
            }         
            try {
                if (this.isLiveStoryTemplateType()) {
                    // Do Nothing
                } else {
                   rval = "";
                }  
            } catch(e) {}
            return rval;
        },
        getCNNSourceID: function(){ //prop44 - Source ID
            var rval = "";
            try {
                if(typeof window.CNN != 'undefined' && typeof window.CNN.omniture != 'undefined' && window.CNN.omniture.sourceId) {
                        rval = window.CNN.omniture.sourceId;
                    } else if(window.CNN && window.CNN.contentModel && window.CNN.contentModel.sourceId){
                        rval = window.CNN.contentModel.sourceId;
                }
                rval = rval.toLowerCase();
            } catch(e) {}
            return rval;    
        },
        getCNNTransactionID: function() { // prop46,eVar46
            var rval = "";
            try {
                if (typeof window.cnnad_transactionID !== 'undefined') {
                    rval = window.cnnad_transactionID;
                } else if (typeof window.cnnad_getTransactionID === "function") {
                    rval = cnnad_getTransactionID();
                } else {
                    rval = Math.round((new Date()).getTime() / 1000) + "" + Math.floor(Math.random()*9007199254740992);
                }
            } catch (e) {}
            return rval;
        },
        getCNNGUID: function() { // prop47,eVar47
            var rval = "";
            try {
                if (typeof window.turner_getGuid === "function") {
                    rval = turner_getGuid("ug");
                } else {
                    rval = this.getCookie("ug");
                }
            } catch (e) {}
            return rval;
        },
        getAppNexusID: function() {
            var rval = "";
            try {
                if (this.isTagConsented("app-nexus-id")) {
                    rval = this.getCookie("zwmc");
                }
            } catch (e) {}
            return rval
        },
        getWMID: function(name) {
            var rval = "";
            try {
                if (window.WM) {
                    var obj = window.WM.PSM || window.WM.CDP || {};
                    var fn = obj["get"+name];
                    if (typeof fn === "function") {
                        rval = fn();
                    }
                }
            } catch (e) {}
            return rval;
        },
        getWMUKID: function() {
            var rval = "";
            try {
                rval = this.getCookie('WMUKID_STABLE');

                if (!rval) {
                    var wmukidJSON = this.getCookie("WMUKID");
                    var wmukidObj = JSON.parse(wmukidJSON);
                    rval = wmukidObj.id;
                }

            } catch (e) {}
            return rval
        },
        getCNNUID: function() {
            return this.getCookie("_cnn_uid");
        },
        getEdition: function() {
            var rsid = _satellite.getVar("RSID");
            var hostName = window.location.hostname;
            if (rsid.includes("esp")) {
                return "espanol";
            } else if (hostName.includes("edition")) {
                return "international";
            } else {
                return "domestic";
            }
        },
        setLinkTrackVars: function(names) {
            if (s.linkTrackVars == "None") return;
            let nameArr = names.split(",");
            nameArr.forEach(name => {
                if (!s.linkTrackVars.includes(name)) {
                    s.linkTrackVars += "," + name;
                }
            });
        },
        mapProp: function(eVarNum) {
            return {
                "26": "pageName",
                "27": "channel",
                "29": "server",
                "41": "prop29"
            } [eVarNum] || ("prop" + eVarNum);
        },
        setProps: function(eVarNums) {
            let eVarNumArr = eVarNums.split(",");
            eVarNumArr.forEach(eVarNum => {
                var eVarKey = "eVar" + eVarNum;
                var propKey = this.mapProp(eVarNum);
                if (s[eVarKey]) {
                    s[propKey] = s[propKey] || s[eVarKey];
                    s[eVarKey] = "D=c" + eVarNum;
                }
            });
        },
        setEVars: function(eVarNums) {
            let eVarNumArr = eVarNums.split(",");
            eVarNumArr.forEach(eVarNum => {
                var propKey = this.mapProp(eVarNum);
                var eVarKey = "eVar" + eVarNum;
                if (s[propKey]) {
                    s[eVarKey] = s[propKey];
                    s[propKey] = "";
                } else {
                    s[eVarKey] = "";
                }
            });
        },
        setIds: function() {
            this.setLinkTrackVars("eVar106,eVar195,eVar197,eVar198,eVar199");
            s.eVar106 = this.getCNNUID();
            s.eVar195 = this.getAppNexusID();
            s.eVar197 = this.getWMUKID();
            s.eVar198 = this.getWMID("WMHHID");
            s.eVar199 = this.getWMID("WMINID");
        },
        setUserAuthState: function() {
            this.setLinkTrackVars("eVar51,eVar74,eVar89");
            s.eVar51 = this.getUserAuthState("registration");
            s.eVar74 = this.getUserAuthState("verification");
            s.eVar89 = this.getUserAuthState("login");
        },
        setCommonVars: function(useProps) {
            this.setLinkTrackVars("pageName,eVar26,server,eVar29,channel,eVar27,prop11,eVar11,prop28,eVar28,prop32,eVar32,prop33,eVar33");
            s.eVar26 = s.eVar26 || wminst.Util.getCNNPageName();
            s.eVar29 = wminst.Util.getADBPURL("domain");
            s.eVar27 = wminst.Util.getCNNSection(0);
            s.eVar11 = wminst.Util.getCNNBrandingPartner();
            s.eVar28 = wminst.Util.getCNNSection(1);
            s.eVar32 = s.eVar32 || wminst.Util.getCNNTemplateType("long");
            s.eVar33 = wminst.Util.getCNNContentType();
            this.setLinkTrackVars("prop30,eVar30,prop35,eVar35");
            s.eVar30 = this.getBusinessUnit();
            s.prop35 = this.getCodeVersion();
            s.eVar35 = "D=c35"
            this.setLinkTrackVars("eVar44");
            s.eVar44 = this.getDL2Prop("vertical").toLowerCase();
            this.setUserAuthState();
            this.setLinkTrackVars("eVar90");
            s.eVar90 = this.getEdition();
            this.setIds();
            this.setLinkTrackVars("eVar111");
            s.eVar111 = this.getCNNLeadingMedia();
            this.setLinkTrackVars("eVar112,eVar113,eVar114,eVar132");
            s.eVar112 = this.getDL2Prop("firstCanonicalUrl");
            s.eVar113 = this.getDL2Prop("pageStellarId");
            s.eVar114 = this.getDL2Prop("pageTags").toLowerCase();
            s.eVar132 = this.getDL2Prop("pageType").toLowerCase();
            this.setLinkTrackVars("list1");
            s.list1 = s.list1 || this.getCNNTopic();
            if (useProps) this.setProps("11,26,27,28,29,30,32,33");
        },
        setPageVars: function() {
            this.setLinkTrackVars("eVar48,eVar129");
            s.eVar48 = this.getCNNTechStack();
            s.eVar129 = this.commentsEnabled() ? "comments available" : "comments not available";
        },
        setVideoVars: function(data, useProps) {
            this.setLinkTrackVars("prop53,eVar53,prop57,eVar57,prop59,eVar59");
            s.eVar53 = this.getLiveStreamName(data);
            s.eVar57 = this.getMVPD(data) || this.getCNNMVPD();
            s.eVar59 = this.getAdobeID(data) || this.getCNNAdobeID();
            this.setLinkTrackVars("eVar104");
            s.eVar104 = data.videoTitleId || data.title_id || "";
            if (data.video_collection) {
                this.setLinkTrackVars("eVar116");
                s.eVar116 = data.video_collection.toLowerCase();
                s.eVar116 += ":" + (data.total_videos || 1);
                s.eVar116 += ":" + (data.video_position || 1);
            }
            this.setLinkTrackVars("eVar117,eVar118,eVar119,eVar120");
            s.eVar117 = data.stellarId || "";
            s.eVar118 = data.parentStellarId || "";
            s.eVar119 = (data.videoTags || []).join(",");
            s.eVar120 = (data.videoUrl || "");
            this.setLinkTrackVars("eVar124,eVar127,eVar130");
            s.eVar124 = (data.branding || "").toLowerCase();
            s.eVar127 = (data.firstPublishSlug || "").toLowerCase();
            s.eVar130 = this.getPreviewType(data);
            if (useProps) this.setProps("53,57,59");
        },
        getCNNTechStack: function() { //eVar48 - Site Tech Stack
            return this.getDL2Prop("techStack").toLowerCase();
        },
        getCNNCMSId: function() { //eVar49 - CMS ID
            var rval = "";
            try {
                if(window.CNN && window.CNN.contentModel && window.CNN.contentModel.cmsId){
                    rval = CNN.contentModel.cmsId;
                }
            } catch(e){}
            return rval;
        },
        getCNNPreviousPageName: function(){ //prop49,eVar49 - Previous PageName
            var rval = "";
            try {
                if(this.isTagConsented('adobe')) {
                    var pName = window.document.referrer;
                    var prevP = s.getPreviousValue(wminst.Util.getCNNPageName(),"cnprevpage_pn");
                    if (prevP && typeof pName != "undefined" && pName != "" && pName.indexOf(".cnn.com") != -1) {
                        return prevP;
                    }
                }
            } catch(e) {return rval;}
            return rval;
        },
        getCNNPostTitle: function() { //prop50 - Post Title
            var rval = "";
            try{
                if(window.CNN && window.CNN.omniture && window.CNN.omniture.post_title) {
                    rval = window.CNN.omniture.post_title;
                } else { 
                    rval = document.title;
                }
            } catch(e) { rval = document.title; }
            rval = rval.toLowerCase();
            try {
                var dom_obj = $x("//script[@type='application/ld+json']");
                var post_obj = JSON.parse(rval[rval.length - 1]).innerHTML;
                if(post_obj && post_obj.headline){
                     rval = post_obj.headline;
                } 
            } catch(e) {}
            try {
                if (this.isLiveStoryTemplateType()) {
                   // Do Nothing
                } else {
                   rval = "";
                }  
            } catch(e) {}
            if(rval !== "") {
                rval = rval.replace(/\([0-9]+\)/, "").trim();
            }
            return rval;
        },
        getLiveStreamName: function(data) {
            var rval = (data.live_stream_name || data.title || "").toLowerCase();
            if (data.id.includes("cvpstream")) {
                rval += " " + data.id.substr(-1);
            }
            return data.isLive ? rval : "";
        },
        getCNNBreakingNewsHP: function(ptt, chnl) {
            var rval = "";
            var tt = "";
            try {
                if (ptt.indexOf(":") != -1) {
                    if (ptt.indexOf("adbp") != -1) {
                        ptt = ptt.split(":");
                        tt = ptt[1];
                    } else {
                        ptt = ptt.split(":");
                        tt = ptt[0];
                    }
                } else {
                    tt = ptt;
                }
                var abr = {
                    "index": "in",
                    "video": "v",
                    "videos": "v",
                    "blog": "b",
                    "blogs": "b",
                    "game": "g",
                    "games": "g",
                    "interactive": "it",
                    "content": "c",
                    "error": "err",
                    "section": "sf",
                    "section front": "sf",
                    "gallery": "ga",
                    "show": "sh",
                    "shows": "sh",
                    "special": "sp",
                    "specials": "sp",
                    "topic": "t",
                    "profile": "p",
                    "article": "c"
                } [tt];
                if (chnl && (chnl == "homepage" || chnl == "cnn homepage")) {
                    chnl = "index";
                }
                if (tt) {
                    rval = "breaking:" + chnl + ":" + abr + ":";
                }
                return rval;
            } catch (e) {}
        },
        getCNNOrientation: function() { //prop56,eVar56 - page orientation
            var rval = "no value set";
            try {
                var x = 0;
                if (self.innerHeight) {
                    x = self.innerWidth;
                } else if (document.documentElement && document.documentElement.clientHeight) {
                    x = document.documentElement.clientWidth;
                } else if (document.body) {
                    x = document.body.clientWidth;
                }
                var y = 0;
                if (self.innerHeight) {
                    y = self.innerHeight;
                } else if (document.documentElement && document.documentElement.clientHeight) {
                    y = document.documentElement.clientHeight;
                } else if (document.body) {
                    y = document.body.clientHeight;
                }
                rval = (y > x) ? "portrait" : "landscape";
            } catch (e) {}
            return rval;
        },
        getPreviewType: function(data) {
            return (data.previewType || "nvs").toLowerCase();
        },
        getMVPD: function(data) {
            return (data.mvpd || data.mvpd_value || "").toLowerCase();
        },
        getAdobeID: function(data) {
            return data.adobe_hash_id || data.adobeHashId || "";
        },
        getCookieFromDL: function(cookieName, propName) {
            var propVal = this.getDataLayerV1()[propName];
            if (propVal) {
                this.setCookie(cookieName, propVal);
            }
            return this.getCookie(cookieName) || "no mvpd set";
        },
        getLocalStorageFromDL: function(keyName, propName) {
            var propVal = this.getDataLayerV1()[propName];
            if (propVal) {
                localStorage.setItem(keyName, propVal);
            }
            return localStorage.getItem(keyName) || "nvs";
        },
        getCNNMVPD: function() {
            return this.getCookieFromDL("CNNmvpd", "mvpd");
        },
        getCNNAdobeID: function() {
            return this.getCookieFromDL("adobe_hash_id", "adobe_hash_id");
        },
        getCNNUserAuthState: function() {
            return this.getLocalStorageFromDL("user_auth_state", "user_auth_state");
        },
        getCNNPlayerState: function(video) { //eVar67 player State
            var screenState = video.screen_state || "nvs";
            var screenPosition = video.screen_position || "nvs";
            var audioState = video.audio_state || "nvs";
            var playerState = "";
            try {
                if (screenState == "nvs" && CNN && CNN.omniture && CNN.omniture.screen_state) {
                    screenState = CNN.omniture.screen_state;
                }
                if (audioState == "nvs") {
                    if (video.muted === true) {
                        audioState = "muted";
                    } else if (video.muted === false) {
                        audioState = "audio on";
                    }
                }
                playerState = screenState + "|" + audioState + "|" + screenPosition;
                playerState = playerState.toLowerCase();
            } catch (e) {}
            return playerState;
        },
        getCNNVisitorID: function(id) { //eVar73 - page visitorId
            var rval = "";
            try {
                rval = _satellite.cookie.get(id);
                rval = rval.replace(/\[(.+?)\]/g, "");
                rval = rval.split("|")[1];
                rval = rval.toLowerCase();
            } catch (err) {}
            return rval;
        },
        getCNNHierachy: function() { // hier1 - Hierachy
            var rval = "";
          /*  try {
                var bUnit = this.getBusinessUnit();
                var channel = this.getCNNSection(0);
                var domain = this.getADBPURL("domain");
                var section2 = this.getCNNSection(1);
                rval = "news|cnn|" + bUnit + "|" + domain + "|" + channel + "|" + section2; 
            } catch(e){} */
            return rval;
        },
        getCNNUIEngagement: function() { //prop64 - UI Engagement
            var rval = (this.isNGTVPage() || this.isTVEPage()) ? "ngtv" : "cnn news";
            try { 
                if(typeof window.cnn_metadata.friendly_name != 'undefined') {
                    rval = window.cnn_metadata.friendly_name;
                }
            } catch(e) {}
            return rval;
        },
        getCNNTopicAvailability: function() {
            var topic_pattern = new RegExp(/^[0-9a-z,]+$/);
            try {
                var rval = wminst.Util.getCNNTopic();
                if(rval == ""){
                    return "no topics";
                } else if(topic_pattern.test(rval)) {
                    return "topics available";
                } else { 
                    return "api request failure";
                }
            } catch(e) {}
        },
        getCNNTopic: function() {
            let topicObj = (window.CNN || {}).cep_topics || {};
            let topicKeys = ["cep_brsf", "cep_iabt", "cep_sent", "cep_tags"];
            let topicVals = [];
            for (let [key, val] of Object.entries(topicObj)) {
                if (topicKeys.includes(key)) topicVals = topicVals.concat(val);
            }
            let topicStr = (window.cna_omniture || {}).topic || "";
            return (topicVals.toString() || topicStr).toLowerCase();
        },
        getCEPTopisForVideo: function(data) {
            let topicObj = (data || {}).cepTopics || {};
            let topicKeys = Object.keys(topicObj);
            return topicKeys.toString().toLowerCase();
        },
        getCNNSiteSectionLevel3: function(val) { //prop51 - Site section level 3 for politics
            var rval = "";
            try {
                rval = wminst.Util.getCNNSection(1);
                if(typeof val != 'undefined') {
                    rval += ":" + val;
                } else if(CNN && CNN.omniture && CNN.omniture.section && typeof CNN.omniture.section[2] != 'undefined') {
                    rval += ":" + CNN.omniture.section[2];
                }
            } catch (e) {}
            return rval;
        },
        getCNNInteractiveState: function(data) { //eVar50 - Interactive State for politics
            var rval = "";
            if(typeof data == 'undefined' && window.location.hash === "#my_election") {
                rval = "election center:my election:panel open";
                return rval;
            }
            if (typeof data == "object" && (typeof data.tab != 'undefined' || typeof data.map_state != 'undefined' || typeof data.map_level != 'undefined')) {
                var tab = data.tab || "nvs";
                var map_state = data.map_state || "nvs";
                if(!wminst.Util.isPoliticsExplorer()) {
                    if (typeof data.action != 'undefined') {
                        var map_level = data.map_level || "nvs";
                        var race_type = data.race_type || "nvs";
                        var overlay_type = data.overlay_type || "nvs";
                        var show_by = data.show_by || "nvs";
                        rval = "ec:" + race_type + ":" + map_level + ":" + overlay_type + ":" + show_by;
                    }
                    else
                        rval = "election center:" + tab + ":" + map_state;
                } else {
                    var year = data.year || "nvs";
                    var comparison_layer = data.comparison_layer || "nvs";
                    var e_val = data.election || "nvs";
                    rval = tab + ":" + year + ":" + e_val + ":" + comparison_layer + ":" + map_state;
                }
                rval = rval.toLowerCase();
            }
            return rval
        },
        getSiteSpecificSettings: function(type, section) {
            var hostName = window.location.hostname;
            var port = window.location.port;
            var setting;
            var sites = {
                "cnn": ["cnn-adbp-domestic", "cnn domestic", "cnn", "metrics.cnn.com", "smetrics.cnn.com", "us-100120", "b01", "00001", "8587204"],
                "cnndev": ["cnn-adbp-domestic-dev", "cnn domestic", "cnn", "metrics.cnn.com", "smetrics.cnn.com", "us-100120", "b01", "00001", "8587204"],
                "cnnintl": ["cnn-adbp-intl", "cnn international", "cnn", "metrics.cnn.com", "smetrics.cnn.com", "us-100120", "b01", "00002", "8587278"],
                "cnnintldev": ["cnn-adbp-intl-dev", "cnn international", "cnn", "metrics.cnn.com", "smetrics.cnn.com", "us-100120", "b01", "00002", "8587278"],
                "ireport": ["cnnireport-adbp", "cnn ireport", "cnnireport", "metrics.cnn.com", "smetrics.cnn.com", "us-702210", "c01", "00001", "3002212"],
                "ireportdev": ["cnnireport-adbp-dev", "cnn ireport", "cnnireport", "metrics.cnn.com", "smetrics.cnn.com", "us-702210", "c01", "00001", "3002212"]
            }

            var c4 = {
                val1: ["cnn homepage", "8587211", "8587278"],
                val2: ["crime", "8587220"],
                val3: ["us", "8587228"],
                val4: ["world", "8587235"],
                val5: ["entertainment", "8587242"],
                val6: ["politics", "8587248"],
                val7: ["health", "8587254"],
                val8: ["tech", "8587261"],
                val9: ["living", "8587266"],
                val10: ["opinion", "8587272"],
                val11: ["watch cnn", "8587204"]
            }

            if (section && section != "") {
                var x = 0;
                for (x in c4) {
                    if (c4[x][0] == section) {
                        setting = c4[x][1];
                        if (section == "cnn homepage") {
                            if (hostName.indexOf("edition.cnn.com") != -1) {
                                setting = c4[x][2];
                            } else if (hostName.indexOf("jcmsdev8.cnn.com") != -1 || hostName.indexOf("jcmsref.cnn.com") != -1 || hostName.indexOf("cnnpreview.cnn.com") != -1 || hostName.indexOf("ref.cnn.com") != -1 || hostName.indexOf("preview.cnn.com") != -1) {
                                if (port.indexOf("94") != -1 || hostName.indexOf("edition") != -1) {
                                    setting = c4[x][2];
                                }
                            }
                        }
                        break;
                    }
                }
            } else {
                if (hostName.indexOf("ireportqa.cnn.com") != -1) {
                    setting = sites.ireportdev[type];
                } else if (hostName.indexOf("jcmsdev8.cnn.com") != -1 || hostName.indexOf("jcmsref.cnn.com") != -1 || hostName.indexOf("cnnpreview.cnn.com") != -1 || hostName.indexOf("ref.cnn.com") != -1 || hostName.indexOf("preview.cnn.com") != -1 || hostName.indexOf("dev.cnn.com") != -1 || hostName.indexOf("stage.cnngo.com") != -1 || hostName.indexOf("travel.cnngo.com") != -1 || hostName.indexOf("edition.stage.next.cnn.com") != -1 || hostName.indexOf("cnnpreview.turner.com") != -1 || hostName.indexOf("dev.cnnv2.com") != -1 || hostName.indexOf("ref.cnnv2.com") != -1 || hostName.match(/^(dev|qa|stage).(www|us|edition)-m.cnn.com/) || hostName.indexOf("edition.enable.next.cnn.com") != -1 || hostName.indexOf("terra.next.cnn.com") != -1 || hostName.indexOf("politics.next.cnn.com") !== -1 || hostName.indexOf("edition.politics.next.cnn.com") !== -1) {
                    if (port.indexOf("94") != -1 || hostName.indexOf("edition") != -1 || hostName.indexOf("cnnespanol") != -1 || hostName.indexOf("stage.cnngo.com") != -1 || hostName.indexOf("travel.cnngo.com") != -1) {
                        setting = sites.cnnintldev[type];
                    } else {
                        setting = sites.cnndev[type];
                    }
                } else if (hostName.indexOf("qai.cnn.com") != -1) {
                    setting = sites.cnndev[type];
                } else if (hostName.indexOf("cnn.staging.perfectmarket.com") != -1 || hostName.indexOf("cnn.staging2.perfectmarket.com") != -1 || hostName.indexOf("beta-cronkite.cnnlabs.com") != -1 || hostName.indexOf("dev-audioplayer-cnn.s3.amazonaws.com") != -1) {
                    setting = sites.cnndev[type];
                } else if (hostName.indexOf("darwin-dev.hope.ui") != -1 || hostName.indexOf("dev-facts-first.cnnlabs.com")!= -1) {
                    setting = sites.cnndev[type];
                } else if (hostName.indexOf("int-facts-first.cnnlabs.com") != -1) {
                    setting = sites.cnnintldev[type];
                } else if (hostName.indexOf("ireport.cnn.com") != -1) {
                    setting = sites.ireport[type];
                } else if (hostName.indexOf("edition.cnn.com") != -1 || hostName.indexOf("cnnespanol.cnn.com") != -1 || hostName.indexOf("backstory.blogs.cnn.com") != -1 || hostName.indexOf("inthefield.blogs.cnn.com") != -1 || hostName.indexOf("securityfiles.blogs.cnn.com") != -1 || hostName.indexOf("thecnnfreedomproject.blogs.cnn.com") != -1 || hostName.indexOf("ukelection.blogs.cnn.com") != -1 || hostName.indexOf("amanpour.blogs.cnn.com") != -1 || hostName.indexOf("screeningroom.blogs.cnn.com") != -1 || hostName.indexOf("internationaldesk.blogs.cnn.com") != -1 || hostName.indexOf("newsstream.blogs.cnn.com") != -1 || hostName.indexOf("prism.blogs.cnn.com") != -1 || hostName.indexOf("thebrief.blogs.cnn.com") != -1 || hostName.indexOf("insidethemiddleeast.blogs.cnn.com") != -1 || hostName.indexOf("connecttheworld.blogs.cnn.com") != -1 || hostName.indexOf("business.blogs.cnn.com") != -1 || hostName.indexOf("questmeansbusiness.blogs.cnn.com") != -1 || hostName.indexOf("goalmouth.blogs.cnn.com") != -1 || hostName.indexOf("olympics.blogs.cnn.com") != -1 || hostName.indexOf("worldsport.blogs.cnn.com") != -1 || hostName.indexOf("bodareal.blogs.cnn.com") != -1 || hostName.indexOf("travel.cnn.com") != -1 || hostName.indexOf("footballclub.cnn.com") != -1 || hostName.indexOf("edition.cnnv2.com") != -1 || hostName.indexOf("edition-m.cnn.com") != -1) {
                    setting = sites.cnnintl[type];
                } else if (hostName.indexOf("cnn.com") != -1 || hostName.indexOf("cnnv2.com") != -1) {
                    setting = sites.cnn[type];
                } else if (hostName.indexOf("fave.api.cnn.io") != -1 || hostName.indexOf("fave-api.cnn.com") != -1) {
                    setting = sites.cnn[type];
                } else if (hostName.indexOf("style.staging.cnn.io") != -1) {
                    setting = sites.cnndev[type];
                } else {
                    //default, if any case failed
                    setting = sites.cnn[type];
                }
            }
            try {
                if (window.CNNIntlVideo) {
                    setting = sites.cnnintl[type];
                }
            } catch (e) {}
            return setting;
        },
        getADBPURL: function(type, lvl) {
            var hostname = window.location.hostname.toLowerCase();
            var pathname = window.location.pathname.toLowerCase();
            var path_array = "";
            pathname = pathname.replace(/([^\/]+\.[^\/]+$)/, "");

            var rval;
            switch (type) {
                case "domain":
                    hostname = hostname.replace("www.", "");
                    if (lvl == parseFloat(lvl)) {
                        var domain_array = hostname.split(".");
                        var currentPointer = domain_array.length - lvl;
                        var currentDomainLevel = (currentPointer >= 0 ? domain_array[currentPointer] : "");
                        rval = currentDomainLevel;
                    } else {
                        rval = hostname;
                    }
                    break;
                case "path":
                    var pathname2 = pathname.substring(1);
                    path_array = pathname2.split("/");
                    if (lvl == parseFloat(lvl) && lvl >= 1) {
                        var currentPathname = (path_array.length >= lvl ? path_array[lvl - 1] : "");
                        rval = currentPathname;
                    } else {
                        rval = pathname;
                    }
                    break;
                case "hier":
                    hostname = hostname.replace("www.", "");
                    path_array = pathname.substring(1).split("/");
                    var h1 = hostname + "/" + path_array[0];
                    var h2 = h1;
                    if (path_array[1]) h2 = h2 + "/" + path_array[1];
                    rval = [h1, h2];
                    break;
                default:
                    rval = hostname + pathname;
            }
            return rval;
        },
        getCNNVideoSequence: function() {
            return "1";
        },
        getUserAuthState: function(type) {
            var userAuthToken = this.getCookieWithDomain("_cnn_at");
            var acctVerified = this.base64Decode(userAuthToken).includes("cnn.authn");
            switch (type) {
                case "registration" : return userAuthToken ? "registered" : "anonymous";
                case "verification" : return acctVerified ? "account verified" : "account not verified";
                case "login"        : return userAuthToken ? "logged in" : "not logged in";
                default             : return "";
            }
        },
        getCNNSavedRaces: function() {
            var rval = "";
            if(typeof CNN != 'undefined' && typeof CNN.saved_races == "number") {
                rval = "election center:save races:" + CNN.saved_races;
            } else {
                if(wminst.Util.getCNNCapContentType()) {
                    rval = "D=c13";
                }
            }
            return rval;
        },
        getCNNExploreIndentify: function(data) { //eVar79 for Politics Explorer
            var rval = "cnn login not required";
            if((data.interaction_type == "year race" && data.racePremiumContent) || (data.interaction_type == "add layer" && data.overlayPremiumContent)) {
                rval = "cnn login required";
            }
            return rval;
        }
    }
}();
wminst.Util.loadCustomVariables();

});</script><script data-anno-uid="anno-uid-z6k2lx3n7dk">_satellite["_runScript2"](function(event, target, Promise) {
// JSMD Adapter to provide backward compatibility
window._jsmd = window._jsmd || {
  init: function() {
    this.mdata = {
      business: {
        cnn: {
          page: {
            author: wminst.Util.getCNNAuthor(),
            branding_content_partner: wminst.Util.getCNNBrandingPartner(),
            section: [wminst.Util.getCNNSection(0), wminst.Util.getCNNSection(1)]
          }
        }
      }
    };
    return this;
  },
  send: function() {
  },
  trackMetrics: function(action, data, map) {
    setTimeout(function() {
      console.log("jsmd adapter trackMetrics action =" + action + " window.trackMetrics = " + typeof window.trackMetrics);
      window.trackMetrics(action, data);
    }, 100);
  },
  plugin: {
    gQuery: function(name) {
      return wminst.Util.getQueryParam(name);
    },
    gCNNVideoCollection: function() {
      return wminst.getCNNMediaCollection();
    }
  }
};
});</script><script data-anno-uid="anno-uid-0w0mqzzfvji">_satellite["_runScript3"](function(event, target, Promise) {
/*! A simple PubSub in JavaScript - v1.0.0 - 2014-01-12
* https://github.com/bdadam/PubSub
* The MIT License (MIT)
* Copyright (c) 2013 Adam Beres-Deak */
!function(){"use strict";function a(a){if("[object String]"!==Object.prototype.toString.call(a))throw new TypeError("Event is not a string.")}function b(a){if("function"!=typeof a)throw new TypeError("Handler is not a function")}var c={},d={};d.publish=d.pub=function(b){if(a(b),c[b])for(var d={event:b,args:Array.prototype.slice.call(arguments,1)},e=0,f=c[b].length;f>e;e++)c[b][e].apply(d,d.args)},d.subscribe=d.sub=function(d,e){a(d),b(e),(c[d]=c[d]||[]).push(e)},d.unsubscribe=d.unsub=function(){var d,e,f,g,h=Array.prototype.slice.call(arguments);if(h.length>=2){if(d=h[0],e=h[1],a(d),b(e),!c[d])return;for(f=0,g=c[d].length;g>f;f++)c[d][f]===e&&c[d].splice(f,1)}else{e=h[0],b(e);for(d in c)for(f=0,g=c[d].length;g>f;f++)c[d][f]===e&&c[d].splice(f,1)}},"function"==typeof define&&define.amd?define(function(){return d}):"object"==typeof module&&module.exports?module.exports=d:window.PubSub=d}();

window.trackMetrics = function(action, data) {
    var realaction = action,
        realdata = data;
    if (typeof(action) == "object") {
        if (action.type != null) {
            realaction = action.type;
        }
        if (action.action != null) {
            realaction = action.action;
        }
        if (action.data != null) {
            realdata = action.data;
        }
    }
    if (typeof(realdata) == "object") {
        if (realdata.data != null) {
            realdata = realdata.data;
        }
    }
    var counter = 0;
    (function poll() {
        if (wminst.subscribersReady || counter >= 10) {
            wminst.Util.log("trackMetrics subscribersReady =", wminst.subscribersReady, "counter =", counter, "action =", realaction, "data =", realdata);
            PubSub.publish(realaction, realdata);
            return true;
        }
        counter++;
        setTimeout(poll, 100);
    })();
 
    //Handling ComScore Events here
    window.trackCSMetrics(realaction, realdata);
};

window.trackCSMetrics = function (realaction, realdata) {
    if ((window.ns_ || {}).StreamingTag) {
        publishCSEvents(realaction, realdata);
    } else {
        wminst.Util.log("trackCSMetrics load comscore streamsense");
        wminst.Util.loadScript("//s.cdn.turner.com/analytics/comscore/streamsense.5.2.0.160629.min.js", function () {
            publishCSEvents(realaction, realdata);
        });
    }

    function publishCSEvents(realaction, realdata) {
        try {
            if (["cnnvideo-preroll", "cnnvideo-adcreative-start"].includes(realaction)) {
                PubSub.publish("cs_video-preroll", realdata);
            } else if (["cnnvideo-adcomplete", "cnnvideo-midroll-complete"].includes(realaction)) {
                PubSub.publish("cs_ad-complete", realdata);
            } else if (["cnnvideo-start", "cnnvideo-autostart", "cnnvideo-live", "cnnvideo-autosegment", "cnnvideo-autoepisode", "cnnvideo-episode"].includes(realaction)) {
                PubSub.publish("cs_video-play", realdata);
            } else if ((["cnnvideo-pause"].includes(realaction)) && (realdata.video || {}).paused == true) {
                PubSub.publish("cs_video-pause", realdata);
            } else if ((["cnnvideo-pause"].includes(realaction)) && (realdata.video || {}).paused == false) {
                PubSub.publish("cs_video-resume", realdata);
            } else if (["cnnvideo-complete"].includes(realaction)) {
                PubSub.publish("cs_video-complete", realdata);
            }
        } catch (e) {}
    }
}

window.setINSTVideoEvent = function(event, data) {
    if (event == "cnnvideo-pause" && !data.paused) {
        event = "cnnvideo-resume";
    }
    window.instVideoEvent = {
        name: event,
        time: +(new Date())
    };
};

window.trackVideoEvent = function(data, event, playerid) {
    try {
        if (event !== "cnnvideo-progress") {
            setINSTVideoEvent(event, data);
            var currVidObj = data;
            currVidObj.playerid = playerid;
            trackMetrics({
                type: event,
                data: {
                    video : currVidObj
                }
            });
        }
    } catch (e) {}
};

window.trackVideoProgress = function(vidInfo) {
    try {
        setINSTVideoEvent("cnnvideo-progress", vidInfo);
        trackMetrics({
            type: "cnnvideo-progress",
            data: { video: vidInfo }
        });
    } catch (e) {}
};

window.setINSTAudioEvent = function(event, data) {
    if (event == "audio-pause" && !data.paused) {
        event = "audio-resume";
    }
    window.instAudioEvent = {
        name: event,
        time: +(new Date())
    };
};

window.trackAudioEvent = function(data, event, playerid) {
    try {
        if (event !== "audio-progress") {
            setINSTAudioEvent(event, data);
            var currAudObj = data;
            currAudObj.playerid = playerid;
            trackMetrics({
                type: event,
                data: {
                    audio : currAudObj
                }
            });
        }
    } catch (e) {}
};

window.trackAudioProgress = function(audInfo) {
    try {
        setINSTAudioEvent("audio-progress", audInfo);
        trackMetrics({
            type: "audio-progress",
            data: { audio: audInfo }
        });
    } catch (e) {}
};

window.sendVideoEvent = function(data, event, playerid) {
    try {
        var currVidObj = window.JSON.parse(data);
        currVidObj.playerid = playerid;
        trackMetrics({
            type: event,
            data: {
                video : currVidObj
            }
        });
    } catch (e) {}
};

window.sendAudioEvent = function(data, event, id) {
    try {
        var currAudObj = (typeof data != "string"? data: window.JSON.parse(data));
        trackMetrics({
            type: event,
            data: {
                instance: id,
                audio: currAudObj
            }
        });
    } catch (e) {}
};

window.sendInteractionEvent = function(event, data) {
    try {
        trackMetrics({
            type: event,
            data: {
                interaction: data
            }
        });
    } catch (e) {}
};

window.sendHP10Interaction = function (data) {
    sendInteractionEvent("hp10-interaction", "10minpreview:"+data);
};

window.sendGameInteraction = function(event,info) {
    try {
        trackMetrics({
            type: event,
            data: {
                value: info
            }
        });
    } catch (e) {}
};

window.sendVideoClick = function(info, event) {
    try {
        trackMetrics({
            type: event,
            data: {
                value: info
            }
        });
    } catch (e) {}
};

window.sendNewsPulse = function(data) {
    try {
        trackMetrics({
            type: "dynamic-newsPulseOmniCall",
            data: {
                newspulse: {
                    query: data
                }
            }
        });
    } catch (e) {}
};

window.sendHTML5Event = function(data, event) {
    if (data.contentType =="audio") {
        trackMetrics("audio-start",data.headline, "adbp-audio");
    } else {
        data.metas= {branding:"ireport"};
        try {
            trackMetrics({
                type: event,
                data: {
                    video : data
                }
            });
        } catch (e) {}
    }
};

window.sendOpenStoryPerspective = function(data) {
    try {
        trackMetrics({
            type: "ireport-openstory",
            data: {
                openstory : data
            }
        });
    } catch (e) {}
};

window.trackExitLinkMetrics = function(action) {
    try {
        PubSub.publish(action,"");
    }
    catch (e) {}
};

if (wminst.Util.isStellarPage() && wminst.Util.isUserAccountPage() && window.ZION_MESSAGE_BUS) {
    ZION_MESSAGE_BUS.subscribe("event_published", function(message) {
        try {
            var msgIndex = message.length - 1;
            var eventObj = message[msgIndex].message.event; 
            var eventName = eventObj.name;
            if (eventName == "PaymentTransactionCompleted") {
                var billing_cycle = eventObj.props.billing_interval;
                if (billing_cycle == "monthly" || billing_cycle == "annualy" || billing_cycle == "yearly") {
                    var httpResp = eventObj.props.http_response;
                    wminst.Util.log("eventName =", eventName, "billing =", billing_cycle, "httpResp =", httpResp);
                    if (httpResp == "success") {
                        window.trackMetrics({
                            type: "site_subscription_success",
                            data: eventObj.props
                        });
                    }
                }
            }
        } catch (e) {
            console.error(e);
        }
    })
}
//DOM scrapping to track retailer clicks clicked on CNN underscroed pages on non CNN links
var sendFBRetailClickPixel = function(data) {
    try {
        trackMetrics({
            type: "facebook-retailer-click",
            data: data
        });
    } catch (e) {}
};  
try {
    var elements = document.querySelectorAll('[class*="offer-link"]');
    for (var i = 0; i < elements.length; i++) {
        var data = {};
        var linkText = elements[i].innerText ? elements[i].innerText : elements[i].innerHTML;
        if(typeof elements[i] !== 'undefined' && linkText !== '') {
          data.clickedLink = elements[i].href;
          data.clickedText = linkText;
        }
        elements[i].addEventListener('click', function() {sendFBRetailClickPixel(data);}, false);
    }
} catch (e) {}

});</script><script data-anno-uid="anno-uid-ffdtc0z2dfa">_satellite["_runScript4"](function(event, target, Promise) {
wminst.getVideoMetadata = function(data) {
    return data.video || data;
}

wminst.getAudioMetadata = function(data) {
    return data.audio || data;
}

wminst.isAMPVideos = function() {
    var hostName = window.location.hostname;
    return hostName.indexOf("fave.api.cnn.io") != -1 || hostName.indexOf("fave-api.cnn.com") != -1;
};

wminst.isBusinessVideo = function(v) {
    var sectionName = v.sectionName || v.category || "";
    var sectionNameList = ["media", "intl_business", "tech", "business", "business-videos", "cars", "investing", "success", "perspectives", "homes"];
    return sectionNameList.includes(sectionName);
};

wminst.getAMPVideoTimeStamp = function() {
    var pathName = window.location.pathname;
    var ts = "";
    if (pathName.indexOf("/v1/amp") != -1 || pathName.indexOf("/v1/cnneamp") != -1 || pathName.indexOf("/v1/fbia") != -1 || pathName.indexOf("/v1/fbiaV2") != -1) {
        ts = new Date().getTime();
    }
    return ts;
};

var mediaPlayer = [];
wminst.getCNNMediaCollection = function() {
    return {
        get: function(i, p) {
            var mPlayer = mediaPlayer;
            for (var j = mPlayer.length - 1; j >= 0; j--) {
                if (mPlayer[j].containerId == i) {
                    return mPlayer[j][p];
                }
            }
        },
        set: function(i, p, v) {
            var mPlayer = mediaPlayer;
            for (var j = mPlayer.length - 1; j >= 0; j--) {
                if (mPlayer[j].containerId == i) {
                    mPlayer[j][p] = v;
                    break;
                }
            }
        },
        toggle: function(i, p) {
            var mPlayer = mediaPlayer;
            for (var j = mPlayer.length - 1; j >= 0; j--) {
                if (mPlayer[j].containerId == i) {
                    var v = mPlayer[j][p];
                    mPlayer[j][p] = !v;
                    break;
                }
            }
        },
        start: function(i, t) {
            var mPlayer = mediaPlayer;
            mPlayer.push(new objMediaPlayer(i,t));
            function objMediaPlayer(cid, mediaTitle) {
                this.containerId = cid;
                this.mediaTitle = mediaTitle;
                this.vidStarted = false;
                this.audStarted = false;
                this.hasScrubbed = false;
                this.isAuto = false;
                this.isTen = false;
                this.isTwentyFive = false;
                this.isHalf = false;
                this.isSeventyFive = false;
                this.isNinety = false;
                this.isBuffering = false;
                this.isPaused = false;
                this.isMidrollStarted = false;
                this.adNumber = 0;
                this.startTime = (new Date()).getTime();
                this.currentTime = (new Date()).getTime();
                this.timeSpent = 0;
            }
        },
        pause: function(i) {
            var mPlayer = mediaPlayer;
            for (var j = mPlayer.length - 1; j >= 0; j--) {
                if (mPlayer[j].containerId == i) {
                    var p = mPlayer[j].isPaused;
                    var b = mPlayer[j].isBuffering;
                    if (!b) {
                        if (p) {
                            mPlayer[j].startTime = (new Date()).getTime();
                        } else {
                            var playedTime = (new Date()).getTime() - mPlayer[j].startTime + mPlayer[j].timeSpent;
                            mPlayer[j].timeSpent = playedTime;
                        }
                    }
                    mPlayer[j].isPaused = !p;
                    break;
                }
            }
        },
        buffer: function(i) {
            var mPlayer = mediaPlayer;
            for (var j = mPlayer.length - 1; j >= 0; j--) {
                if (mPlayer[j].containerId == i) {
                    var p = mPlayer[j].isPaused;
                    var b = mPlayer[j].isBuffering;
                    if (!p) {
                        if (b) {
                            mPlayer[j].startTime = (new Date()).getTime();
                        } else {
                            var playedTime = (new Date()).getTime() - mPlayer[j].startTime + mPlayer[j].timeSpent;
                            mPlayer[j].timeSpent = playedTime;
                        }
                    }
                    mPlayer[j].isBuffering = !b;
                    break;
                }
            }
        },
        progress: function(i) {
            var mPlayer = mediaPlayer;
            for (var j = mPlayer.length - 1; j >= 0; j--) {
                if (mPlayer[j].containerId == i) {
                    mPlayer[j].currentTime = (new Date()).getTime();
                    var playedTime = (mPlayer[j].currentTime - mPlayer[j].startTime + mPlayer[j].timeSpent) / 1000;
                    mPlayer[j].startTime = (new Date()).getTime();
                    mPlayer[j].timeSpent = 0;
                    return Math.round(playedTime);
                }
            }
        },
        complete: function(i) {
            var mPlayer = mediaPlayer;
            for (var j = mPlayer.length - 1; j >= 0; j--) {
                if (mPlayer[j].containerId == i) {
                    var playedTime = ((new Date()).getTime() - mPlayer[j].startTime + mPlayer[j].timeSpent) / 1000;
                    mPlayer[j].timeSpent = 0;
                    return Math.round(playedTime);
                }
            }
        }
    };
};

wminst.capCNNTimeSpent = function(timeSpent, trt, liveInterval) {
    try { //check media time spent value
        var timeLimit = 0;
        if ((parseFloat(timeSpent) == parseInt(timeSpent)) && !isNaN(timeSpent)) {
            if (liveInterval && liveInterval > 0) {
                timeLimit = liveInterval; //time limit value set by webdev
            } else {
                timeLimit = 60; //time limit in sec
                if (trt && parseFloat(trt) > 0) {
                    timeLimit = parseFloat(trt) * 2;
                }
            }
            if (timeSpent > timeLimit) {
                timeSpent = timeLimit;
            } else if (timeSpent < 0) {
                timeSpent = 0;
            }
        } else {
            timeSpent = 0;
        }
    } catch (e) {
        timeSpent = 0;
    }
    return timeSpent;
};

wminst.capCNNTimeSpent2 = function(timeSpent, trt) {
    try { //check media time spent value
        if ((parseFloat(timeSpent) == parseInt(timeSpent)) && !isNaN(timeSpent)) { //valid time spent value
            if (trt && !isNaN(trt) && (parseFloat(trt) == parseInt(trt))) { //valid media length
                if (timeSpent > parseFloat(trt) * 2) {
                    timeSpent = parseFloat(trt) * 2;
                } else if (timeSpent < 0) {
                    timeSpent = 0;
                }
            } else { //invalid media length
                timeSpent = 0;
            }
        } else { //invalid time spent value
            timeSpent = 0;
        }
    } catch (e) {
        timeSpent = 0;
    }
    return timeSpent;
};
});</script><script data-anno-uid="anno-uid-vz3ew7h4vl">_satellite["_runScript5"](function(event, target, Promise) {
wminst.comscorePageBeacon = function() {
    var c_id = "6035748";
    var cs_ucfr = wminst.Util.isTagConsented("comscore") ? "1" : "0";
    var params = {
        c1: "2", c2: c_id, cs_ucfr: cs_ucfr,
        options: {
            enableFirstPartyCookie: true
        }
    }
    if (wminst.Util.isFBIAPage() === true) {
        params.options.url_append = "comscorekw=fbia";
    }
    var _comscore = window._comscore = _comscore || [];
    _comscore.push(params);
    
    try {
        if (window.COMSCORE) {
            COMSCORE.beacon(_comscore[0]);
            wminst.Util.sendImagePixel("//lightning.cnn.com/analytics/cnn/comscore-pageview-candidate.json");
        } else {
            wminst.Util.loadScript("https://sb.scorecardresearch.com/cs/" + c_id + "/beacon.js");
        }
    } catch (e) {}
};

PubSub.subscribe("dynamic-page", function(data) {
    wminst.comscorePageBeacon();
});

PubSub.subscribe("tab-page", function(data) {
    wminst.comscorePageBeacon();
});

PubSub.subscribe("cnnsearch-results", function(data) {
    wminst.comscorePageBeacon();
});

PubSub.subscribe("weather-page", function(data) {
    wminst.comscorePageBeacon();
});

PubSub.subscribe("picker-pageview", function(data) {
    wminst.comscorePageBeacon();
});

PubSub.subscribe("cnngallery-click", function(data) {
    wminst.comscorePageBeacon();
});

PubSub.subscribe("readmore-page", function(data) {
    wminst.comscorePageBeacon();
});

PubSub.subscribe("breaking-news", function(data) {
    if (data.domain && (data.domain == "cnn.com" || data.domain == "us.cnn.com" || data.domain == "sweet.next.cnn.com" || data.domain == "edition.cnn.com")) {
        // Do Nothing
    } else {
        wminst.comscorePageBeacon();
    }
});


/* ============== Page Load ============= */
if (!wminst.Util.isDynamicPage() && !wminst.Util.isFavePage() && !wminst.Util.inIFrame()) { 
    wminst.comscorePageBeacon();
}

});</script><script data-anno-uid="anno-uid-bwy8doyz1v">_satellite["_runScript6"](function(event, target, Promise) {
wminst.bomboraStandardVITag = function() {
    if (!window._ml) {
        (function (w,d,t){
         _ml = w._ml || {};
         _ml.nq = w._ml.nq || [];
         _ml.nq.push(['track', '64240', {fp: 'YOUR_USER_ID'}]);
         var s, cd, tag; s = d.getElementsByTagName(t)[0]; cd = new Date();
         tag = d.createElement(t); tag.async = 1;
         tag.src = 'https://cdn.ml314.com/taglw.js';
         s.parentNode.insertBefore(tag, s);
        })(window,document,'script');
    } else {
        _ml.nq = window._ml.nq || [];
        _ml.nq.push(['track', '64240']);
    }
};

wminst.bomboraRealTimeVITag = function() {
    if (!window._bmb) {
        !function(e,t,c,n,o,a,m){e._bmb||(o=e._bmb=function(){o.x?o.x.apply(o,arguments):o.q.push(arguments)},o.q=[],a=t.createElement(c),a.async=true,a.src="https://vi.ml314.com/get?eid=64240&tk=GBYTTE9dUG2OqHj1Rk9DPOaLspvMWfLqV236sdkHgf03d&fp="+(e.localStorage&&e.localStorage.getItem(n)||""),m=t.getElementsByTagName(c)[0],m.parentNode.insertBefore(a,m))}(window,document,"script","_ccmaid");
    }

    window.googletag = window.googletag || {cmd: []};
    googletag.cmd.push(function() {
      _bmb('vi', function(data){
        if (data != null) {
          var tmpSegment = [
            data.industry_id,
            data.revenue_id,
            data.size_id,
            data.functional_area_id,
            data.professional_group_id,
            data.seniority_id,
            data.decision_maker_id,
            data.install_data_id,
            data.topic_id,
            data.interest_group_id,
            data.segment,
            data.b2b_interest_cluster_id
            ].filter(Boolean).join(',');

          tmpSegment != '' && googletag.pubads().setTargeting("bmb",tmpSegment.split(','));
        }
      });
    });
};

wminst.bomboraPageBeacon = function() {
    wminst.bomboraStandardVITag()
    wminst.bomboraRealTimeVITag()
};

PubSub.subscribe("dynamic-page", function(data) {
    wminst.bomboraPageBeacon();
});

PubSub.subscribe("tab-page", function(data) {
    wminst.bomboraPageBeacon();
});

PubSub.subscribe("cnnsearch-results", function(data) {
    wminst.bomboraPageBeacon();
});

PubSub.subscribe("weather-page", function(data) {
    wminst.bomboraPageBeacon();
});

PubSub.subscribe("picker-pageview", function(data) {
    wminst.bomboraPageBeacon();
});

PubSub.subscribe("readmore-page", function(data) {
    wminst.bomboraPageBeacon();
});

PubSub.subscribe("breaking-news", function(data) {
    if (data.domain && (data.domain == "cnn.com" || data.domain == "us.cnn.com" || data.domain == "sweet.next.cnn.com" || data.domain == "edition.cnn.com")) {
        // Do Nothing
    } else {
        wminst.bomboraPageBeacon();
    }
});


/* ============== Page Load ============= */
if (!wminst.Util.isDynamicPage() && !wminst.Util.isFavePage() && !wminst.Util.inIFrame()) { 
    wminst.bomboraPageBeacon();
}
});</script><script data-anno-uid="anno-uid-ty5numcmm2">_satellite["_runScript7"](function(event, target, Promise) {
wminst.initStreamingTag = function () {
    wminst.myStreamingTag = new ns_.StreamingTag({
        customerC2: "6035748"
    });
}

PubSub.subscribe("Player_Ready", function(data) {
    if (typeof wminst.myStreamingTag != "undefined") {
        wminst.myStreamingTag.stop();
    }
    wminst.initStreamingTag();
});

PubSub.subscribe("cs_video-preroll", function(data) {
    var v = wminst.getVideoMetadata(data);
    if (typeof wminst.myStreamingTag != "undefined") {
        wminst.myStreamingTag.stop();
    }
    if (!wminst.prev_vid) { //first video
        wminst.initStreamingTag();
    } else if (wminst.prev_vid && wminst.prev_vid !== v.id) { //new video
        wminst.initStreamingTag();
    } else if (wminst.completed_vid && wminst.completed_vid == v.id) {
        wminst.completed_vid = "";
        wminst.initStreamingTag();
    }
    wminst.prev_vid = v.id;
    var clength = v.ad_duration || 0;
    try {
        clength = parseInt(clength);
        if (clength % 1000 !== 0) {
            clength = clength * 1000;
        }
    } catch (e) {
        clength = 0;
    }
    var cs_ucfr = wminst.Util.isTagConsented("comscore") ? "1" : "0";
    var metadata = {
        ns_st_cl: clength || 3000,
        cs_ucfr: cs_ucfr
    };
    if (ns_) {
        ns_.StreamingTag.AdType = {
            BrandedOnDemandContent: "34",
            BrandedOnDemandLive: "35",
            BrandedOnDemandMidRoll: "32",
            BrandedOnDemandPostRoll: "33",
            BrandedOnDemandPreRoll: "31",
            LinearLive: "21",
            LinearOnDemandMidRoll: "12",
            LinearOnDemandPostRoll: "13",
            LinearOnDemandPreRoll: "11",
            Other: "00"
        };
    }
    var atype = ns_.StreamingTag.AdType.LinearOnDemandPreRoll;
    if (v.adType && v.adType.toLowerCase() === "midroll") { atype = ns_.StreamingTag.AdType.LinearOnDemandMidRoll; }
    if (v.adType && v.adType.toLowerCase() === "postroll") { atype = ns_.StreamingTag.AdType.LinearOnDemandPostRoll; }
    if (v.isLive && (v.isLive == "true" || v.isLive == true)) {
        atype = ns_.StreamingTag.AdType.LinearLive;
    }
    wminst.myStreamingTag.playVideoAdvertisement(metadata, atype);
});

PubSub.subscribe("cs_ad-complete", function(data) {
    if (typeof wminst.myStreamingTag != "undefined") {
        wminst.myStreamingTag.stop();
    }
});

PubSub.subscribe("cs_video-play", function(data) {
    var v = wminst.getVideoMetadata(data);
    if (typeof wminst.myStreamingTag != "undefined") {
        wminst.myStreamingTag.stop();
    }
    if (!wminst.prev_vid) { //first video
        wminst.initStreamingTag();
    } else if (wminst.prev_vid && wminst.prev_vid !== v.id) { //new video
        wminst.initStreamingTag();
    } else if (wminst.completed_vid && wminst.completed_vid == v.id) {
        wminst.completed_vid = "";
        wminst.initStreamingTag();
    }
    wminst.prev_vid = v.id;
    var clength = v.trt || 0;
    var c4 = "CNN";
    var c3 = "*null";
    var c6 = "*null";
    try {
        clength = parseInt(clength);
        if (clength % 1000 !== 0) {
            clength = clength * 1000;
        }
    } catch (e) {
        clength = 0;
    }
    var adate = v.timestamp || "";
    try {
        if (adate) {
            adate = new Date(adate);
            adate = adate.toISOString().substring(0, 10);
        }
    } catch (e) {}
    if (window.location.hostname.indexOf("edition") != -1) {
        c4 = "CNNI";
        c3 = "CNNEDITION";
    }
    if (typeof v.category != 'undefined' && v.category.toLowerCase() === "spanish") {
        c4 = "CNNESPANOL";
    }
    if (typeof v.category != 'undefined' && v.category.toLowerCase() === "cnnmoney") {
        c4 = "CNNMONEY";
    }
    var ch = wminst.Util.getCNNSection(0) || "";
    var pn = {
        "entertainment":    "CNNENT",
        "health":           "CNNHEALTH",
        "politics":         "CNNPOLITICS",
        "tech":             "CNNTECH",
        "travel":           "CNNTRAVEL",
        "us":               "CNNUS",
        "world":            "CNNWORLD",
        "opinions":         "CNNOPINION",
        "living":           "CNNLIVING",
        "cnn homepage":     "CNNHOME",
        "ireport":          "IREPORT",
        "justice":          "CNNJUSTICE",
        "elections":        "CNNPOLITICS",
        "style":            "CNNSTYLE"
    }[ch];
    if (pn) { c4 = pn; }
    if(pn && ch == "elections"){ c6 = "ELECTION";}
    if (wminst.isBusinessVideo(data)) {
        c4 = "CNNBUSINESS";
        c6 = "BUSINESS";
    }
    var cs_ucfr = wminst.Util.isTagConsented("comscore") ? "1" : "0";
    var metadata = {
        ns_st_ci: v.id,
        ns_st_cl: clength,
        ns_st_st: "*null",
        ns_st_pu: "CNN",
        ns_st_pr: v.subcategory || "*null",
        ns_st_ep: v.headline || "*null",
        ns_st_sn: "*null",
        ns_st_en: "*null",
        ns_st_ge: v.category || "*null",
        ns_st_ia: "0",
        ns_st_ce: "0",
        ns_st_ddt: "*null",
        ns_st_tdt: adate || "*null",
        c3: c3,
        c4: c4,
        c6: c6,
        cs_ucfr: cs_ucfr
    };
    if (ns_) {
        ns_.StreamingTag.ContentType = {
            Bumper: "99",
            Live: "13",
            LongFormOnDemand: "12",
            Other: "00",
            ShortFormOnDemand: "11",
            UserGeneratedLive: "23",
            UserGeneratedLongFormOnDemand: "22",
            UserGeneratedShortFormOnDemand: "21"
        };
    }
    var vtype = ns_.StreamingTag.ContentType.ShortFormOnDemand;
    if (v.content_type && v.content_type == "episode") {
        vtype = ns_.StreamingTag.ContentType.LongFormOnDemand;
    }
    if (v.id && v.id.indexOf("cvplive") != -1) {
        vtype = ns_.StreamingTag.ContentType.Live;
    }
    if (v.isLive && v.isLive == "true") {
        vtype = ns_.StreamingTag.ContentType.Live;
    }
    wminst.myStreamingTag.playVideoContentPart(metadata, vtype);
});
PubSub.subscribe("cs_video-pause", function(data) {
    if (typeof wminst.myStreamingTag != "undefined") {
        wminst.myStreamingTag.stop();
    }
});
PubSub.subscribe("cs_video-resume", function(data) {
    var v = wminst.getVideoMetadata(data);
    if (typeof wminst.myStreamingTag != "undefined") {
        wminst.myStreamingTag.stop();
    }

    var clength = v.trt || 0;
    var c4 = "CNN";
    var c3 = "*null";
    var c6 = "*null";
    try {
        clength = parseInt(clength);
        if (clength % 1000 !== 0) {
            clength = clength * 1000;
        }
    } catch (e) {
        clength = 0;
    }
    var adate = v.timestamp || "";
    try {
        if (adate) {
            adate = new Date(adate);
            adate = adate.toISOString().substring(0, 10);
        }
    } catch (e) {}
    if (window.location.hostname.indexOf("edition") != -1) {
        c4 = "CNNI";
        c3 = "CNNEDITION";
    }
    if (typeof v.category != 'undefined' && v.category.toLowerCase() === "spanish") {
        c4 = "CNNESPANOL";
    }
    if (typeof v.category != 'undefined' && v.category.toLowerCase() === "cnnmoney") {
        c4 = "CNNMONEY";
    }
    var ch = wminst.Util.getCNNSection(0) || "";
    var pn = {
        "entertainment":    "CNNENT",
        "health":           "CNNHEALTH",
        "politics":         "CNNPOLITICS",
        "tech":             "CNNTECH",
        "travel":           "CNNTRAVEL",
        "us":               "CNNUS",
        "world":            "CNNWORLD",
        "opinions":         "CNNOPINION",
        "living":           "CNNLIVING",
        "cnn homepage":     "CNNHOME",
        "ireport":          "IREPORT",
        "justice":          "CNNJUSTICE",
        "elections":        "CNNPOLITICS",
        "style":            "CNNSTYLE"
    }[ch];
    if (pn) { c4 = pn; }
    if(pn && ch == "elections"){ c6 = "ELECTION";}
    if (wminst.isBusinessVideo(data)) {
        c4 = "CNNBUSINESS";
        c6 = "BUSINESS";
    }
    var cs_ucfr = wminst.Util.isTagConsented("comscore") ? "1" : "0";
    var metadata = {
        ns_st_ci: v.id,
        ns_st_cl: clength,
        ns_st_st: "*null",
        ns_st_pu: "CNN",
        ns_st_pr: v.subcategory || "*null",
        ns_st_ep: v.headline || "*null",
        ns_st_sn: "*null",
        ns_st_en: "*null",
        ns_st_ge: v.category || "*null",
        ns_st_ia: "0",
        ns_st_ce: "0",
        ns_st_ddt: "*null",
        ns_st_tdt: adate || "*null",
        c3: c3,
        c4: c4,
        c6: c6,
        cs_ucfr: cs_ucfr
    };
    if (ns_) {
        ns_.StreamingTag.ContentType = {
            Bumper: "99",
            Live: "13",
            LongFormOnDemand: "12",
            Other: "00",
            ShortFormOnDemand: "11",
            UserGeneratedLive: "23",
            UserGeneratedLongFormOnDemand: "22",
            UserGeneratedShortFormOnDemand: "21"
        };
    }
    var vtype = ns_.StreamingTag.ContentType.ShortFormOnDemand;
    if (v.content_type && v.content_type == "episode") {
        vtype = ns_.StreamingTag.ContentType.LongFormOnDemand;
    }
    if (v.id && v.id.indexOf("cvplive") != -1) {
        vtype = ns_.StreamingTag.ContentType.Live;
    }
    if (v.isLive && v.isLive == "true") {
        vtype = ns_.StreamingTag.ContentType.Live;
    }
    wminst.myStreamingTag.playVideoContentPart(metadata, vtype);
});

PubSub.subscribe("cs_video-complete", function(data) {
    var v = wminst.getVideoMetadata(data);
    wminst.completed_vid = v.id;
    if (typeof wminst.myStreamingTag != "undefined") {
        wminst.myStreamingTag.stop();
    }
});

PubSub.subscribe("Video_Completed", function(data) {
    var v = wminst.getVideoMetadata(data);
    wminst.completed_vid = v.id;
    if (typeof wminst.myStreamingTag != "undefined") {
        wminst.myStreamingTag.stop();
    }
});
});</script><script data-anno-uid="anno-uid-7vkgfz18r9">_satellite["_runScript8"](function(event, target, Promise) {
wminst.nielsenPageBeacon = function() {
    var ci, si, rp, random;
    ci = "us-204044h";
    si = escape(window.location.href);
    rp = escape(document.referrer);
    random = +(new Date());
    wminst.Util.sendImagePixel("//secure-us.imrworldwide.com/cgi-bin/m?ci=" + ci + "&cg=0&cc=1&si=" + si + "&rp=" + rp +"&ts=compact&rnd=" + random);
};

if (!wminst.Util.isRefreshPage() && !wminst.Util.inIFrame()) {
    wminst.nielsenPageBeacon();
}
});</script><script data-anno-uid="anno-uid-c0bma7ctped">_satellite["_runScript9"](function(event, target, Promise) {
wminst.nielsenVideoBeacon = function(state, data, cg) {
    var v = wminst.getVideoMetadata(data);
    var ci, c6, tl, random, url;
    ci = "us-100120";
    c6 = (v.category && (v.category == "cnnmoney" || v.category == "business")) ? "vc,c02" : "vc,b01";
    tl = state + "-" + v.id;
    random = +(new Date());
    url = "//secure-us.imrworldwide.com/cgi-bin/m?ci=" + ci + "&c6=" + c6 + "&cc=1&tl=" + tl + "&rnd=" + random;
    if (cg) url += "&cg=" + cg;
    wminst.Util.sendImagePixel(url);
};

PubSub.subscribe("cnnvideo-start", function(data) {
    wminst.nielsenVideoBeacon("dav0", data);
});

PubSub.subscribe("cnnvideo-autostart", function(data) {
    wminst.nielsenVideoBeacon("dav0", data);
});

PubSub.subscribe("cnnvideo-live", function(data) {
    wminst.nielsenVideoBeacon("dav0", data, "live");
});

PubSub.subscribe("cnnvideo-episode", function(data) {
    wminst.nielsenVideoBeacon("dav0", data);
});

PubSub.subscribe("cnnvideo-complete", function(data) {
    wminst.nielsenVideoBeacon("dav2", data);
});
});</script><script data-anno-uid="anno-uid-nxyl3w1mo1">_satellite["_runScript10"](function(event, target, Promise) {
function checkUserAuthentication(){var e="";return window.is_expansion||(e=void 0!==s.prop32&&s.prop32.includes("interactive")?wminst.Util.getCNNAuthenticated("authid","displayname","reg:logged in","requires authentication","reg:not logged in","?"):void 0!==s.prop28&&"watch cnn:activation"==s.prop28?wminst.Util.getCNNAuthenticated("authid","displayname","reg:logged in","does not require authentication","reg:not logged in","?"):wminst.Util.getCNNAuthenticated("authid","displayname","reg:logged in","anonymous","reg:not logged in","?")),e}wminst.trackPage=function(){wminst.Util.setCommonVars(!0),wminst.Util.setPageVars(),s.t()},wminst.trackLink=function(e){wminst.Util.setCommonVars(!1),s.tl(this,"o",e)},wminst.getSocialClick=function(e){var t=e.interaction||e.clickObj||{},r="string"==typeof t?t:t.socialType||"";return(r=r.replace(": ",":")).startsWith("social")||(r="social:"+r),r.endsWith("click")||(r+="_click"),wminst.Util.isFactsFirstPage()&&(r=r.replace("social:","facts first:share:")),t.isMainNav&&(r+=":global"),t.component&&t.socialType&&t.action&&(r=t.component+":"+t.socialType+":"+t.action),r},wminst.getInteractionType=function(e){var t="";return"priceless xi"==e.branding_social?t="priceless xi":"politics:submit debate topics"==e.interaction?t="debate topic submission":s.prop69&&(t=s.prop69),t},wminst.waitAfterInteraction=function(e){"account nav:topics you can follow"==e.interaction&&wminst.Util.wait(50)},wminst.setBounceX=function(e){if(e.bouncex&&(s.prop62=e.bouncex.toLowerCase(),s.linkTrackEvents=s.linkTrackEvents+",event20",s.events=s.linkTrackEvents,""!==s.prop62)){let e=s.events.split(",");for(let t=0;t<=e.length;t++)"event26"!==e[t]&&"event39"!==e[t]&&"event76"!==e[t]&&"event21"!==e[t]||(e.splice(t,1),t=0);s.linkTrackEvents=e.toString(),s.events=s.linkTrackEvents,s.linkTrackVars="events,campaign,eVar36,eVar59,prop59,prop62,eVar62,eVar73,prop73,list2"}},wminst.setOnboarding=function(e,t){"onboarding"==e.page&&(s.pageName=t,s.prop69="registration onboarding",e.interaction&&(s.prop69+=":"+e.interaction),e.newsletter&&(s.prop69+=":"+e.newsletter))},wminst.setModuleLoad=function(e){if("module load"==e.interaction){wminst.Util.setLinkTrackVars("eVar122,eVar123"),s.linkTrackEvents="event117";let r=(e.componentName||"").toLowerCase();if(r.includes("follow topic")){s.linkTrackEvents="event116";let t=e.followTopicNames||[];for(let e=0;e<t.length;e++){r+="|"+(e+1)+"|"+(t[e]||"").toLowerCase()}}else if(e.componentAttributes){var t=e.componentAttributes||{};s.prop69=[t.type,t.apiType,t.locationOnPage,t.numberOfItems,t.title].join(":").toLowerCase()}else e.engagementNumber?s.prop69=["alerts","web push banner","module engagement number",e.engagementNumber].join(":"):e.componentType&&e.componentViewCount&&(s.prop69=[e.componentType,e.componentViewCount].join(":"));s.events=s.linkTrackEvents,s.eVar122=r,s.eVar123=e.componentStellarId||""}},wminst.setFollowTopic=function(e){e.interaction.includes("follow topic")&&(wminst.Util.setLinkTrackVars("eVar121,eVar125"),e.interaction.includes("follow all topics")?(s.eVar121=(e.followTopicNames||[]).toString().toLowerCase(),s.eVar125=(e.followTopicIds||[]).toString()):(s.eVar121=e.followTopicName.toLowerCase()||"",s.eVar125=e.followTopicId||""))},wminst.getErrorMessage=function(e){var t=[];return(e.addtData||e).errorMessage?.data?.forEach((e=>{t.push(e.message?.toLowerCase())})),t.join()},wminst.getLSPostInteraction=function(e){var t=e.isDeepLink?"deeplink":"not deeplink";return["live story",e.postNumber,e.totalPosts,e.tabView,e.sortType,e.postType,t].join(":").toLowerCase()},wminst.trackArticleViewed=function(e){s.manageVars("clearVars"),s.linkTrackVars="events,eVar36,prop59,eVar59,prop69,eVar69,prop73,eVar73,list2";var t={"article start":"event43","article 25":"event44","article 50":"event46","article 75":"event47","article complete":"event57"}[e.interaction];t&&(s.linkTrackEvents=t+",event76",s.events=s.linkTrackEvents,s.eVar36=wminst.Util.getCNNKruxID(),s.prop59=wminst.Util.getCNNAdobeID(),s.prop69=wminst.Util.getCNNTemplateType("long")+":"+e.interaction,wminst.trackLink(e.interaction),s.clearVars())},wminst.trackUserAccount=function(e){s.manageVars("clearVars"),s.linkTrackVars="events,eVar36,prop59,eVar59,prop69,eVar69,prop73,eVar73,list2,eVar131";var t={"account created":"event52","logged in":"event54","logged out":"event101","login failure":"event102","registration failure":"event103"}[e.action];if(t){s.linkTrackEvents=t+",event76",s.events=s.linkTrackEvents,s.eVar36=wminst.Util.getCNNKruxID(),s.prop59=wminst.Util.getCNNAdobeID(),s.prop69="cnn account:"+e.action,e.method&&(s.prop69+=":"+e.method.toLowerCase());var r=wminst.getErrorMessage(e);r&&(s.prop69+=":"+r),s.eVar131=(e.method||"").toLowerCase(),wminst.trackLink(s.prop69),s.clearVars()}},wminst.trackLiveStoryPost=function(e){s.manageVars("clearVars"),s.linkTrackVars="events,eVar36,prop43,prop50,prop59,eVar59,prop69,eVar69,prop73,eVar73,list2",s.linkTrackEvents="event121",s.events=s.linkTrackEvents,s.eVar36=wminst.Util.getCNNKruxID(),s.prop43=e.postId||"",s.prop50=(e.postTitle||"").toLowerCase(),s.prop59=wminst.Util.getCNNAdobeID(),s.prop69=wminst.getLSPostInteraction(e.interaction),wminst.trackLink(s.prop69),s.clearVars()},PubSub.subscribe("dynamic-autoRefresh",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,eVar36,eVar37,prop44,eVar45,prop46,eVar46,prop47,eVar47,prop69,eVar69,prop73,eVar73,list2",s.linkTrackEvents="event60",s.events=s.linkTrackEvents,s.eVar36=wminst.Util.getCNNKruxID(),s.eVar37=wminst.Util.getCNNPlatform(),s.prop44=wminst.Util.getCNNSourceID(),s.prop46=wminst.Util.getCNNTransactionID(),s.prop47=wminst.Util.getCNNGUID(),s.prop69=e,s.prop73=wminst.Util.getCNNVisitorID("s_vi"),wminst.trackLink("auto-refresh"),s.clearVars()})),PubSub.subscribe("dynamic-page",(function(e){if((wminst.Util.isTravelPage()||wminst.Util.isStylePage())&&!wminst.Util.isLiveStoryPage())return wminst.trackPage();s.manageVars("clearVars"),s.linkTrackVars="events,hier1,prop2,eVar2,prop4,eVar4,prop5,eVar5,prop14,eVar14,prop15,eVar15,eVar22,prop23,eVar23,prop43,prop44,eVar45,prop48,prop50,eVar50,prop51,prop64,eVar64,eVar65,prop73,eVar73,prop75,eVar75,eVar79,eVar105,list2",s.linkTrackEvents="event26",s.events=s.linkTrackEvents;var t=e.clickObj||{};if(t.socialType){var r=s.pageName;if(r.match(/\s\[.+\]$/)){var a=/(.+)\s\[.+\]$/.exec(r);a&&(r=a[1])}s.pageName=r+" ["+t.socialType+"]"}if(e.pageURL){try{e.pageURL.split("/")[2].replace("www.",""),e.pageURL=e.pageURL.toLowerCase(),e.pageURL=e.pageURL.replace(/^.*\/\/[^\/]+/,""),e.pageURL=e.pageURL.replace("/index.html","/"),s.pageName=wminst.Util.getCNNPageName(e.pageURL)}catch(e){}}void 0!==window.CNN&&void 0!==window.CNN.omniture&&void 0!==window.CNN.omniture.section&&"facts first"==window.CNN.omniture.section[1]&&(s.linkTrackEvents=s.linkTrackEvents+",event59",s.events=s.linkTrackEvents),s.pageURL=wminst.Util.getCNNPageURL();try{var i="",n="",o="";n=wminst.Util.getCNNPublishDate(),i=wminst.Util.getCNNDaysSinceLastPublish("a");var p=["content:","live story"];o=wminst.Util.getCNNTemplateType("long");var c=!1;if(o&&void 0!==o){for(var l in p)-1!=o.indexOf(p[l])&&(c=!0);c?(s.prop10=i,s.prop16=n):(s.prop10="",s.prop16="")}if(void 0!==window.CNN.omniture&&void 0!==window.CNN.omniture.branding_social)try{s.prop14=window.CNN.omniture.branding_social||""}catch(e){}s.prop23=wminst.Util.getCNNPageHeadline(),"ngtv"==wminst.Util.getCNNUIEngagement()&&(s.prop57=e.mvpd,s.prop59=e.adobe_hash_id)}catch(e){}var m="",V="";if(void 0!==e.headline)try{window.CNN=window.CNN||{},window.CNN.omniture=window.CNN.omniture||{},window.CNN.omniture.section=e.section,window.CNN.omniture.template_type=e.template_type,window.CNN.omniture.branding_content_page=e.branding_content_page,window.CNN.omniture.branding_social=e.branding_social,window.CNN.omniture.cap_author=e.cap_author,window.CNN.omniture.cap_genre=e.cap_genre,window.CNN.omniture.cap_content_type=e.cap_content_type,window.CNN.omniture.cap_topic=e.cap_topic,window.CNN.contentModel=window.CNN.contentModel||{},window.CNN.contentModel.analytics=window.CNN.contentModel.analytics||{},window.CNN.contentModel.analytics.pageTop=e.page_top||{},window.CNN.contentModel.analytics.isArticleVideoCollection=e.is_article_video_collection||!1,window.CNN.omniture.user_auth_state=e.user_auth_state,V=wminst.Util.getCNNDaysSinceLastPublish(e.publish_date),s.prop10=V+"",s.prop14=e.branding_social,s.prop14&&""!==s.prop14&&(s.events="event24,"+s.events),wminst.Util.addBrandingEvent(),s.linkTrackEvents=s.events,s.prop16=e.publish_date,s.prop23=e.headline.toLowerCase(),s.channel=e.section[0],m=e.section[0]+":"+(e.section[1]?e.section[1]:"nvs"),s.prop28=m,wminst.Util.addArticleEvent(),s.linkTrackEvents=s.events,e.load_type&&"lazy_load"==e.load_type&&(s.events="event26,event72",s.linkTrackEvents=s.events),e.load_type&&"refresh_load"==e.load_type&&(s.events="event26,event71",s.linkTrackEvents=s.events)}catch(e){}try{s.prop64=wminst.Util.getCNNUIEngagement(),s.prop2=wminst.Util.getCNNAuthor(),wminst.Util.setPageAttribution(),s.prop5=wminst.Util.getCNNCapGenre(),s.prop8=wminst.Util.getCNNVisitNumber(),s.eVar15=wminst.Util.getCNNTrafficPartner(),s.eVar22=wminst.Util.getCNNVideoOpportunity(),s.prop26=wminst.Util.getCNNBaseURL(),s.eVar36=wminst.Util.getCNNKruxID(),s.prop37=wminst.Util.getCNNPlatform(),s.prop43=wminst.Util.getCNNPostID(),s.prop44=wminst.Util.getCNNSourceID(),s.eVar45=wminst.Util.getLSPostPosition(),s.prop48=wminst.Util.getCNNTopicAvailability(),s.prop50=wminst.Util.getCNNPostTitle(),s.prop51=wminst.Util.getCNNSiteSectionLevel3(),s.prop46=wminst.Util.getCNNTransactionID(),s.prop47=wminst.Util.getCNNGUID(),s.prop49=wminst.Util.getCNNPreviousPageName(),s.prop56=wminst.Util.getCNNOrientation(),s.prop57=wminst.Util.getCNNMVPD(),s.prop59=wminst.Util.getCNNAdobeID(),s.prop75=wminst.Util.getCNNUserAuthState(),s.hier1=wminst.Util.getCNNHierachy()}catch(e){}try{if(wminst.Util.isPoliticsExplorer()&&(s.eVar50=wminst.Util.getCNNInteractiveState(e),s.prop51=wminst.Util.getCNNSiteSectionLevel3("explorer"),s.eVar79=wminst.Util.getCNNExploreIndentify(e)),e.interaction_type&&-1!=e.interaction_type.indexOf("road-to-270")){var N=e.interaction_type.split(":");s.pageName=s.pageName+"["+N[2].toLowerCase()+"]",s.prop51=wminst.Util.getCNNSiteSectionLevel3("road-to-270")}}catch(e){}"onboarding"==e.page&&(e.pathName&&(s.pageName+=e.pathName),e.viewName&&(s.pageName+="/"+e.viewName)),wminst.trackPage()})),PubSub.subscribe("refresh_load",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,hier1,prop2,eVar2,prop4,eVar4,prop5,eVar5,prop14,eVar14,prop15,eVar15,eVar22,prop23,eVar23,prop43,prop44,eVar45,prop48,prop50,eVar50,prop51,prop64,eVar64,eVar65,prop73,eVar73,prop75,eVar75,eVar79,eVar105,list2",s.events="event26,event71",s.linkTrackEvents=s.events,s.prop2=wminst.Util.getCNNAuthor(),wminst.Util.setPageAttribution(),s.prop5=wminst.Util.getCNNCapGenre(),s.prop8=wminst.Util.getCNNVisitNumber(),s.prop10=wminst.Util.getCNNDaysSinceLastPublish("a"),s.eVar15=wminst.Util.getCNNTrafficPartner(),s.prop16=wminst.Util.getCNNPublishDate(),s.eVar22=wminst.Util.getCNNVideoOpportunity(),s.prop26=wminst.Util.getCNNBaseURL(),s.eVar36=wminst.Util.getCNNKruxID(),s.prop37=wminst.Util.getCNNPlatform(),s.prop44=wminst.Util.getCNNSourceID(),s.eVar45=wminst.Util.getLSPostPosition(),s.prop46=wminst.Util.getCNNTransactionID(),s.prop47=wminst.Util.getCNNGUID(),s.prop48=wminst.Util.getCNNTopicAvailability(),s.prop49=wminst.Util.getCNNPreviousPageName(),s.prop51=wminst.Util.getCNNSiteSectionLevel3(),s.prop56=wminst.Util.getCNNOrientation(),s.prop57=wminst.Util.getCNNMVPD(),s.prop59=wminst.Util.getCNNAdobeID(),s.prop64=wminst.Util.getCNNUIEngagement(),s.prop75=wminst.Util.getCNNUserAuthState(),s.hier1=wminst.Util.getCNNHierachy();try{s.prop23=e.headline.toLowerCase(),s.prop43=e.post_id,s.prop50=e.post_title.toLowerCase()}catch(e){}wminst.trackPage(),s.clearVars()})),PubSub.subscribe("dynamic-link",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,list2",s.linkTrackEvents="event26",s.events=s.linkTrackEvents,wminst.trackLink(e.link_name),s.clearVars()})),PubSub.subscribe("tab-page",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,prop44,prop51,list2",s.linkTrackEvents="event26",s.events=s.linkTrackEvents,s.prop44=wminst.Util.getCNNSourceID(),s.prop51=wminst.Util.getCNNSiteSectionLevel3();try{s.pageName="cnn:v:/video/"+e}catch(e){}s.pageURL=wminst.Util.getCNNPageURL(),wminst.trackPage(),s.clearVars()})),PubSub.subscribe("cnnsearch-results",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,prop8,eVar8,eVar15,eVar22,prop26,prop27,eVar36,prop37,eVar37,prop39,eVar39,prop44,prop46,eVar46,prop47,eVar47,prop59,eVar59,prop64,eVar64,prop73,eVar73,prop75,eVar75,hier1,list2",s.linkTrackEvents="event26,event27",s.events=s.linkTrackEvents,s.prop8=wminst.Util.getCNNVisitNumber(28),s.eVar15=wminst.Util.getCNNTrafficPartner(),s.eVar22=wminst.Util.getCNNVideoOpportunity(),s.prop26=wminst.Util.getCNNBaseURL(),s.prop27=e.search_results_count+"",s.eVar36=wminst.Util.getCNNKruxID(),s.prop37=wminst.Util.getCNNPlatform();try{e.search_term=e.search_term.replace(/\+/g," "),e.search_term=e.search_term.trim(),e.search_term=e.search_term.toLowerCase()||"empty search"}catch(e){}s.prop39=e.search_term,s.prop44=wminst.Util.getCNNSourceID(),s.prop46=wminst.Util.getCNNTransactionID(),s.prop47=wminst.Util.getCNNGUID(),s.prop49=wminst.Util.getCNNPreviousPageName(),s.prop56=wminst.Util.getCNNOrientation(),s.prop57=wminst.Util.getCNNMVPD(),s.prop59=wminst.Util.getCNNAdobeID(),s.prop64=wminst.Util.getCNNUIEngagement(),s.prop75=wminst.Util.getCNNUserAuthState(),s.hier1=wminst.Util.getCNNHierachy(),s.pageURL=wminst.Util.getCNNPageURL(),wminst.trackPage(),s.clearVars()})),PubSub.subscribe("weather-page",(function(){s.manageVars("clearVars"),s.linkTrackVars="events,prop44,list2",s.linkTrackEvents="event62",s.events=s.linkTrackEvents,s.prop44=wminst.Util.getCNNSourceID(),s.pageURL=wminst.Util.getCNNPageURL(),wminst.trackPage(),s.clearVars()})),PubSub.subscribe("dynamic-impressions",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,prop18,eVar18,list2",s.linkTrackEvents="event26",s.events=s.linkTrackEvents;try{s.prop18=e.value}catch(e){}s.eVar18="D=c18";try{wminst.trackLink(e.link_name+"")}catch(e){}s.clearVars()})),PubSub.subscribe("breaking-news",(function(e){s.linkTrackVars="events,prop4,eVar4,prop8,eVar8,prop16,eVar16,eVar22,eVar36,prop37,eVar37,prop46,eVar46,prop47,eVar47,prop56,eVar56,prop57,eVar57,prop59,eVar59,prop64,eVar64,prop69,eVar69,prop73,eVar73,prop75,eVar75,list2";var t=wminst.Util.getCNNBreakingNewsHP(s.prop32,s.channel);s.pageURL=wminst.Util.getCNNPageURL(),s.prop4=t+e.headline.toLowerCase(),s.eVar36=wminst.Util.getCNNKruxID(),s.prop69=e.item,s.manageVars("clearVars","prop16,eVar16,prop44,prop55,eVar55",1),!e.domain||"cnn.com"!=e.domain&&"us.cnn.com"!=e.domain&&"sweet.next.cnn.com"!=e.domain&&"edition.cnn.com"!=e.domain?(s.linkTrackEvents="event76",s.events=s.linkTrackEvents,wminst.trackPage()):(s.linkTrackEvents="event26",s.events=s.linkTrackEvents),s.clearVars()})),PubSub.subscribe("picker-pageview",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,campaign,heir1,prop8,eVar8,prop26,prop34,evar34,eVar36,prop37,eVar37,prop44,prop46,eVar46,prop47,eVar47,eVar49,eVar49,prop56,eVar56,prop59,eVar59,eVar72,prop75,eVar75,list2",s.linkTrackEvents="event26",s.events=s.linkTrackEvents,s.prop1=s.eVar1=s.prop2=s.eVar2=s.prop3=s.eVar3=s.prop4=s.eVar4=s.prop6=s.eVar6=s.eVar10=s.prop16=s.eVar16=s.prop18=s.eVar18=s.prop31=s.eVar31=s.eVar41=s.eVar53=s.eVar54=s.prop64=s.eVar64=s.prop67=s.eVar67=s.prop68=s.eVar68=s.prop69=s.eVar69=s.prop73=s.eVar73="",s.pageName="cnn:o:["+(e.page_name||"")+"]",s.channel="tve",s.pageURL=wminst.Util.getCNNPageURL(),s.prop8=wminst.Util.getCNNVisitNumber(28),s.prop26=wminst.Util.getCNNBaseURL(),s.prop28="tve:picker",s.prop34=checkUserAuthentication(),s.eVar36=wminst.Util.getCNNKruxID(),s.prop37=wminst.Util.getCNNPlatform(),s.prop44=wminst.Util.getCNNSourceID(),s.prop46=wminst.Util.getCNNTransactionID(),s.prop47=wminst.Util.getCNNGUID(),s.prop49=wminst.Util.getCNNPreviousPageName(),s.prop56=wminst.Util.getCNNOrientation(),s.prop59=wminst.Util.getCNNAdobeID();try{s.prop72=e.free_preview}catch(e){}s.prop32="none",s.eVar72=s.prop72,s.prop72="","cnn:o:[tve: successful login]"==s.pageName?(s.prop7=s.eVar7=s.prop10=s.eVar10=s.eVar22=s.prop23=s.eVar23=s.prop25=s.eVar25=s.eVar65="",s.linkTrackEvents="event37",s.events=s.linkTrackEvents,s.eVar56=s.prop56,s.prop56="",s.eVar57=s.prop57,s.prop57="",s.eVar59=s.prop59,s.prop59="",s.hier1=""):(s.prop57=s.eVar57="",s.prop59=s.eVar59="");try{s.prop75=wminst.Util.getCNNUserAuthState()}catch(e){}wminst.setinterval_id&&clearInterval(wminst.setinterval_id),wminst.trackPage(),s.clearVars()})),PubSub.subscribe("picker-click",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,prop14,eVar14,prop34,eVar34,eVar36,prop37,eVar37,prop46,eVar46,prop47,eVar47,eVar56,eVar57,eVar59,prop69,eVar69,eVar72,prop75,eVar75,list2",s.linkTrackEvents="event76",s.events=s.linkTrackEvents,s.eVar26="cnn:o:["+(e.page_name||"")+"]",s.channel="tve",s.prop28="tve:picker",s.eVar36=wminst.Util.getCNNKruxID(),s.prop37=wminst.Util.getCNNPlatform(),s.prop46=wminst.Util.getCNNTransactionID(),s.prop47=wminst.Util.getCNNGUID(),s.eVar56=wminst.Util.getCNNOrientation(),s.prop56="";try{s.eVar57=e.tve_mvpd.toLowerCase(),s.prop69="tve:picker:"+e.tve_mvpd.toLowerCase()}catch(e){}s.eVar59="no mvpd set";try{s.eVar72=e.free_preview}catch(e){}s.prop73=s.eVar73="";try{s.prop75=wminst.Util.getCNNUserAuthState()}catch(e){}wminst.trackLink("picker-click:"+e.tve_mvpd.toLowerCase()),s.clearVars()})),PubSub.subscribe("social-click",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,prop14,eVar14,eVar36,prop43,prop50,prop59,eVar59,prop69,eVar69,prop73,eVar73,list2",s.linkTrackEvents="event76",s.events=s.linkTrackEvents,s.eVar36=wminst.Util.getCNNKruxID(),s.prop43=wminst.Util.getCNNPostID(),s.prop50=(e.clickObj?.headline||"").toLowerCase(),s.prop14=(e.clickObj||{}).branding_ad,s.eVar14="",s.prop59=wminst.Util.getCNNAdobeID(),s.prop69=wminst.getSocialClick(e);var t=s.prop69.replace("social:","");wminst.trackLink("social-click:"+t),s.clearVars()})),PubSub.subscribe("cnngallery-click",(function(e){if(s.manageVars("clearVars"),s.linkTrackVars="events,prop2,eVar2,prop4,eVar4,prop5,eVar5,prop6,eVar6,prop8,eVar8,prop10,eVar10,eVar15,eVar22,prop23,eVar23,prop25,eVar25,prop26,eVar36,prop37,eVar37,prop44,prop46,eVar46,prop47,eVar47,prop54,eVar54,prop56,eVar56,prop57,eVar57,prop59,eVar59,prop64,eVar64,prop73,eVar73,prop75,eVar75,hier1,list2",s.linkTrackEvents="event26",s.events=s.linkTrackEvents,s.prop2=wminst.Util.getCNNAuthor(),void 0!==e.hpt){var t=e.hpt;try{-1==t.indexOf("_")&&(t=wminst.Util.base64Decode(t))}catch(e){}t=(t=t.replace(/no-value-set/g,"nvs")).toLowerCase(),s.prop4=t}if(s.prop5=wminst.Util.getCNNCapGenre(),s.prop8=wminst.Util.getCNNVisitNumber(28),s.eVar15=wminst.Util.getCNNTrafficPartner(),s.eVar22=wminst.Util.getCNNVideoOpportunity(),s.prop23=wminst.Util.getCNNPageHeadline(),s.prop26=wminst.Util.getCNNBaseURL(),s.eVar36=wminst.Util.getCNNKruxID(),s.prop37=wminst.Util.getCNNPlatform(),void 0!==e.hpt2){var r=e.hpt2;try{-1==r.indexOf("_")&&(r=wminst.Util.base64Decode(r))}catch(e){}r=r.replace(/no-value-set/g,"nvs"),s.prop18=r}s.prop6=(e.gallery_name||"").toLowerCase(),s.prop25=(e.gallery_name||"nvs").toLowerCase().replace(/(no-value-set|no value set)/g,"nvs"),s.prop54="photo gallery:";var a=0;if(void 0!==e.gallery_type&&(s.prop33=e.gallery_type,"carousel"==e.gallery_type)){a=1,s.prop6="",s.eVar6="",s.prop25="",s.eVar25="";var i="";try{i=e.content_type.replace("carousel_","")}catch(e){}void 0!==e.carousel_type||"jumbotron"==e.carousel_type?(s.prop33="jumbotron",s.prop54="jumbotron:"+i):s.prop54="carousel:"+i}if(void 0!==e.pageURL){try{e.pageURL=e.pageURL.toLowerCase(),e.pageURL=e.pageURL.replace(/^.*\/\/[^\/]+/,""),e.pageURL=e.pageURL.replace("/index.html","/")}catch(e){}s.pageName=wminst.Util.getCNNPageName(e.pageURL)}if(void 0!==e.initial_page&&1==e.initial_page?s.prop25=s.eVar25="":1==a?(s.linkTrackEvents="event26,event67",s.events=s.linkTrackEvents):(s.linkTrackEvents="event5,event26",s.events=s.linkTrackEvents),wminst.Util.addBrandingEvent(),s.linkTrackEvents=s.events,s.prop57="no mvpd set",s.prop59=s.prop57,s.prop64=wminst.Util.getCNNUIEngagement(),"ngtv"==s.prop64){s.linkTrackEvents="",s.events="",s.prop32="gallery";try{s.prop57=e.mvpd}catch(e){}try{s.prop57=e.adobe_hash_id}catch(e){}}var n=e.publish_date||"a";s.prop10=wminst.Util.getCNNDaysSinceLastPublish(n),s.prop44=wminst.Util.getCNNSourceID(),s.prop46=wminst.Util.getCNNTransactionID(),s.prop47=wminst.Util.getCNNGUID(),s.prop56=wminst.Util.getCNNOrientation(),s.prop75=wminst.Util.getCNNUserAuthState(),wminst.trackPage(),s.clearVars()})),PubSub.subscribe("photo-page",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,prop4,eVar4,prop6,eVar6,prop8,eVar8,eVar15,eVar22,prop23,eVar23,prop25,eVar25,prop26,eVar36,prop37,eVar37,prop44,prop46,eVar46,prop47,eVar47,prop54,eVar54,prop56,eVar56,prop57,eVar57,prop59,eVar59,prop64,eVar64,prop73,eVar73,prop75,eVar75,eVar105,hier1,list2",s.linkTrackEvents="event26",wminst.Util.setPageAttribution(),s.events=s.linkTrackEvents;var t="";try{t=window.cnn_metadata.business.cnn.page.photo_gallery}catch(e){}try{t=window.CNN.omniture.gallery_name||t}catch(e){}if(t&&(t=t.replace(/%20/g," ")),s.prop6=t,s.prop8=wminst.Util.getCNNVisitNumber(28),s.eVar15=wminst.Util.getCNNTrafficPartner(),s.eVar22=wminst.Util.getCNNVideoOpportunity(),s.prop23=wminst.Util.getCNNPageHeadline(),s.prop26=wminst.Util.getCNNBaseURL(),s.eVar36=wminst.Util.getCNNKruxID(),s.prop37=wminst.Util.getCNNPlatform(),s.prop44=wminst.Util.getCNNSourceID(),s.prop46=wminst.Util.getCNNTransactionID(),s.prop47=wminst.Util.getCNNGUID(),s.prop56=wminst.Util.getCNNOrientation(),s.prop57="no mvpd set",s.prop59=wminst.Util.getCNNAdobeID(),s.prop64=wminst.Util.getCNNUIEngagement(),s.prop75=wminst.Util.getCNNUserAuthState(),1==wminst.isInit)s.prop25="",wminst.isInit=!1;else{s.linkTrackEvents=null,s.events=s.linkTrackEvents,s.eVar6="";try{e.img=e.img+""}catch(e){}try{e.before=e.before+""}catch(e){}e.img?(s.prop25=e.img+"",s.linkTrackEvents="event5",s.events=s.linkTrackEvents,0):e.before&&(s.prop25=e.before+"",s.linkTrackEvents="event5",s.events=s.linkTrackEvents,0),s.prop33="other:gallery"}s.prop25=s.prop25.toLowerCase(),s.eVar1=s.eVar7=s.eVar61=s.eVar68=s.eVar71=s.eVar41="",e.title?wminst.trackLink("photo-page:"+e.title):e.caption&&wminst.trackLink("photo-page:"+e.caption),s.clearVars()})),PubSub.subscribe("ngtv-interaction",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,campaign,eVar34,eVar36,eVar37,prop46,eVar46,prop47,eVar47,prop55,eVar55,eVar57,prop59,eVar59,eVar64,prop69,eVar69,list2",s.linkTrackEvents="event76",s.events=s.linkTrackEvents,s.campaign=wminst.Util.getQueryParam("cid"),s.eVar32="interactive";try{s.eVar34=e.auth_state}catch(e){}s.evar36=wminst.Util.getCNNKruxID(),s.eVar37=wminst.Util.getCNNPlatform(),s.prop46=wminst.Util.getCNNTransactionID(),s.prop47=wminst.Util.getCNNGUID();try{s.eVar57=e.mvpd}catch(e){}s.prop59=wminst.Util.getCNNAdobeID(),s.eVar64=s.prop64,s.prop64="";try{s.prop69=e.interaction}catch(e){}wminst.trackLink("ngtv-interaction:"+e.interaction),s.clearVars()})),PubSub.subscribe("user-interaction",(function(e){var t=s.pageName;if(s.manageVars("clearVars"),s.linkTrackEvents="event26",s.events=s.linkTrackEvents,s.prop28&&-1!=s.prop28.indexOf("electoral college map")?s.prop69=e.interaction+"_click":"comment-click:cronkite"==e.interaction?s.prop69="time shift: on comment":"Go-Live:cronkite"==e.interaction?s.prop69="time shift: go live":"time shift: on video"==e.interaction?s.prop69="time shift: on video":"video carousel"===e.interaction?s.prop69=e.interaction+":click":s.prop69=e.interaction.toLowerCase(),s.prop14=e.branding_social||"",s.campaign=wminst.Util.getQueryParam("cid"),s.eVar36=wminst.Util.getCNNKruxID(),s.eVar37=wminst.Util.getCNNPlatform(),s.prop46=wminst.Util.getCNNTransactionID(),s.prop59=wminst.Util.getCNNAdobeID(),e.pageURL){try{e.pageURL.split("/")[2].replace("www.",""),e.pageURL=e.pageURL.toLowerCase(),e.pageURL=e.pageURL.replace(/^.*\/\/[^\/]+/,""),e.pageURL=e.pageURL.replace("/index.html","/")}catch(e){}s.pageName=wminst.Util.getCNNPageName(e.pageURL)}if(null!==e.interaction.match(/^(travel|style):gallery:(open|viewall)$/)?(s.linkTrackEvents=s.linkTrackEvents+",event30",s.events=s.linkTrackEvents):(s.linkTrackEvents=s.linkTrackEvents+",event76",s.events=s.linkTrackEvents),"politics:submit debate topics"==e.interaction&&(s.prop69=e.interaction),void 0!==s.prop69&&""!==s.prop69){s.eVar69="D=c69",-1!==s.prop69.indexOf("subscribe")?s.linkTrackVars="events,eVar69,prop69,list2":-1!==s.prop28.indexOf("electoral college map")?s.linkTrackVars="events,campaign,eVar36,prop59,eVar59,prop69,eVar69,prop73,eVar73,list2":-1!==s.prop28.indexOf("general elections 2016")?s.linkTrackVars="events,campaign,eVar36,prop69,eVar69,list2":-1!==s.prop69.indexOf("style:menu")?s.linkTrackVars="events,campaign,eVar36,prop59,eVar59,prop69,eVar69,prop73,eVar73,list2":-1!==s.prop69.indexOf("style:gallery:open")?s.linkTrackVars="events,campaign,prop16,eVar16,eVar36,prop59,eVar59,prop69,eVar69,prop73,eVar73,list2":s.linkTrackVars="events,campaign,eVar23,eVar36,prop69,eVar69,prop73,eVar73,list2";let e=s.events.split(",");for(let t=0;t<=e.length;t++)"event26"!==e[t]&&"event21"!==e[t]&&"event39"!==e[t]||(e.splice(t,1),t=0);s.linkTrackEvents=e.toString(),s.events=s.linkTrackEvents}wminst.setBounceX(e),wminst.setOnboarding(e,t),wminst.setModuleLoad(e),wminst.setFollowTopic(e),wminst.trackLink("user interaction:"+wminst.getInteractionType(e)),wminst.waitAfterInteraction(e),s.clearVars()})),PubSub.subscribe("election-click",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,eVar13,eVar50,prop51,prop69,eVar69,eVar79,list2",s.linkTrackEvents="event76",s.events=s.linkTrackEvents,s.pageURL=wminst.Util.getCNNPageURL();var t=void 0!==e.interaction_type?e.interaction_type:"election center:"+e.section,r=void 0!==e.interaction_type?e.interaction_type:"election center:";e.interaction_type&&(r=t=e.interaction_type),void 0!==e.tab&&""!=e.tab&&(t=t+":"+e.tab,r+="tab click"),void 0!==e.area&&""!=e.area&&(t=t+":"+e.area+":click",r="election center:map click"),void 0!==e.action&&""!=e.action&&(-1!=e.action.indexOf("timeline")?(t+=":timeline",r="election center:timeline"):-1!=e.action.indexOf("expanded")&&void 0!==e.issue&&""!=e.issue&&(t=t+":"+e.issue,r="election center:issues")),void 0!==e.button&&""!=e.button&&(t=t+":"+e.button+":click",r="election center:"+e.button+" click");try{void 0!==e.race_type&&void 0!==e.action&&("map click"==e.action||"breadcrumb"==e.action?(s.eVar50=wminst.Util.getCNNInteractiveState(e),t="ec:"+e.race_type+":"+e.state+":"+(e.county||"nvs")+":"+e.action):t="follow"==e.action||"unfollow"==e.action?"ec:"+e.race_type+":"+e.state+":"+e.action:"ec:"+e.race_type+":"+e.action,r=t.toLowerCase()),wminst.Util.isPoliticsExplorer()&&(s.eVar50=wminst.Util.getCNNInteractiveState(e),s.prop51=wminst.Util.getCNNSiteSectionLevel3("explorer"),s.eVar79=wminst.Util.getCNNExploreIndentify(e),r=t="year race"===e.interaction_type?"explorer:"+e.tab+":"+e.interaction_type+":"+e.electionId+":click":"explorer:"+e.tab+":"+e.interaction_type+":click"),e.interaction_type&&-1!=t.indexOf("road-to-270")&&(r=t=e.interaction_type,s.prop51=wminst.Util.getCNNSiteSectionLevel3("road-to-270"))}catch(e){}try{"undefined"==typeof CNN||"number"!=typeof CNN.saved_races||!e.interaction_type||-1==t.indexOf("ec:my election: close panel")&&-1==t.indexOf("ec:my election: open panel")||(s.eVar13="election center: save races:"+t.split(":")[3])}catch(e){}"race-ratings"!=e.page&&"results"!=e.page||(t="ec:"+e.page+":",e.state&&(t+=e.state+":"),r=(t+=e.race+":"+e.action+":"+e.action_detail).toLowerCase());try{s.prop69=t.toLowerCase()}catch(e){}s.eVar69="D=c69",wminst.trackLink(r.toLowerCase()),s.clearVars()})),PubSub.subscribe("election-hover",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,eVar50,prop51,prop69,eVar69,eVar79,list2",s.linkTrackEvents="event76",s.events=s.linkTrackEvents,s.pageURL=wminst.Util.getCNNPageURL();var t=void 0!==e.section?e.section:"",r=void 0!==e.tab?e.tab:"",a=void 0!==e.area?e.area:"",i="election center:"+t+":"+r+":"+(void 0!==e.stateCode?e.stateCode:"")+":"+a+":hover",n="election center:hover";try{void 0!==e.tab&&void 0!==e.map_type&&(n=(i="ec:"+e.tab+":"+e.map_type+":"+e.state+":"+(""==e.county?"nvs":e.county)+":hover").toLowerCase()),wminst.Util.isPoliticsExplorer()&&(s.eVar50=wminst.Util.getCNNInteractiveState(e),s.prop51=wminst.Util.getCNNSiteSectionLevel3("explorer"),s.eVar79=wminst.Util.getCNNExploreIndentify(e),n=(i="explorer:"+e.tab+":"+e.state+":"+(""==e.county?"nvs":e.county)+":hover").toLowerCase())}catch(e){}try{s.prop69=i.toLowerCase(),s.prop69?s.eVar69="D=c69":s.prop69=s.evar69=""}catch(e){}wminst.trackLink(n),s.clearVars()})),PubSub.subscribe("quiz-interaction",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,prop69,eVar69,list2",s.linkTrackEvents="event76",s.events=s.linkTrackEvents;var t=e.clickObj||{};s.prop32="interactive",s.prop33="other:quiz",s.prop69=t.action,wminst.trackLink("quiz-interaction:"+s.prop69),s.clearVars()})),PubSub.subscribe("hp10-interaction",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,eVar36,prop56,eVar56,prop69,eVar69,prop73,eVar73,list2",s.linkTrackEvents="event76",s.events=s.linkTrackEvents,s.eVar36=wminst.Util.getCNNKruxID(),s.prop56=wminst.Util.getCNNOrientation();try{s.prop69=e.interaction}catch(e){}try{wminst.trackLink("hp10-interaction:"+s.prop69)}catch(e){}s.clearVars()})),PubSub.subscribe("trackExitLink-click",(function(){s.manageVars("clearVars"),s.events="event61",s.linkTrackEvents=s.events,s.linkTrackVars="events,eVar36,prop47,eVar47",s.eVar36=wminst.Util.getCNNKruxID(),s.prop47=wminst.Util.getCNNGUID(),s.eVar47="D=c47",wminst.Util.setCommonVars(!1)})),PubSub.subscribe("readmore-click",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,eVar23,eVar36,prop56,eVar56,prop59,eVar59,prop69,eVar69,prop73,eVar73,list2",s.linkTrackEvents="event76",s.eVar23=s.prop23,s.prop23="",s.events=s.linkTrackEvents,s.eVar36=wminst.Util.getCNNKruxID(),s.prop56=wminst.Util.getCNNOrientation(),s.prop59=wminst.Util.getCNNAdobeID();try{s.prop69=e.interaction,e.interaction&&""!=e.interaction&&"facts first:click:read more"==e.interaction&&(s.linkTrackVars="events,eVar23,eVar36,prop56,eVar56,prop59,eVar59,prop69,eVar69,prop73,eVar73,eVar84,eVar85,list2",s.eVar84=e.factcheck_id.toLowerCase()||"",s.eVar85=e.factcheck_headline.toLowerCase()||"")}catch(e){}try{wminst.trackLink("readmore-click:"+s.prop69),s.eVar84=s.eVar85=""}catch(e){}void 0!==window.CNN&&void 0!==window.CNN.omniture&&"facts first"!==window.CNN.omniture.section[1]&&window.sendInteractionEvent("readmore-page",e.interaction),s.clearVars()})),PubSub.subscribe("readmore-page",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,prop2,eVar2,prop4,evar4,prop8,eVar8,eVar15,prop16,eVar16,prop44,prop46,eVar46,prop47,eVar47,prop56,eVar56,prop57,eVar57,prop59,eVar59,prop64,eVar64,prop69,eVar69,prop73,eVar73,prop75,eVar75,eVar105,list2",s.linkTrackEvents="event26",s.events=s.linkTrackEvents,s.prop2=wminst.Util.getCNNAuthor(),wminst.Util.setPageAttribution(),s.prop8=wminst.Util.getCNNVisitNumber(28),s.eVar15=wminst.Util.getCNNTrafficPartner(),wminst.Util.addArticleEvent(),s.linkTrackEvents=s.events,s.pageURL=wminst.Util.getCNNPageURL(),s.prop44=wminst.Util.getCNNSourceID(),s.prop46=wminst.Util.getCNNTransactionID(),s.prop47=wminst.Util.getCNNGUID(),s.prop56=wminst.Util.getCNNOrientation(),s.prop57=wminst.Util.getCNNMVPD(),s.prop59=wminst.Util.getCNNAdobeID(),s.prop64=wminst.Util.getCNNUIEngagement(),s.prop75=wminst.Util.getCNNUserAuthState(),s.eVar3=s.eVar7=s.prop34=s.eVar34=s.eVar41=s.eVar42=s.eVar66=s.eVar67=s.eVar68=s.prop70=s.eVar70=s.eVar71="";try{s.prop69=e.interaction}catch(e){}wminst.trackPage(),s.clearVars()})),PubSub.subscribe("ribbon-interaction",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,eVar36,prop59,eVar59,prop69,eVar69,prop73,eVar73,list2",s.linkTrackEvents="event76,event72",s.events=s.linkTrackEvents,s.eVar36=wminst.Util.getCNNKruxID(),s.prop59=wminst.Util.getCNNAdobeID();var t=e.interaction;try{s.prop69=e.interaction}catch(e){}try{"string"==typeof t&&(t=t.replace(":"," ")),wminst.trackLink(t)}catch(e){}s.clearVars()})),PubSub.subscribe("site-registration_verification",(function(e){PubSub.publish("site-registration",e)})),PubSub.subscribe("site-registration",(function(e){s.manageVars("clearVars"),
s.linkTrackVars="events,eVar36,prop59,eVar59,prop69,eVar69,prop73,eVar73,list2",s.eVar36=wminst.Util.getCNNKruxID(),s.prop59=wminst.Util.getCNNAdobeID(),void 0!==e.action&&(e.action.indexOf("account not successfully")>-1?(s.prop69="user:"+e.action,s.linkTrackEvents="event58,event76",s.events=s.linkTrackEvents,wminst.trackLink(e.action)):e.action.indexOf("account  verified")>-1&&(s.prop69="user:"+e.action,s.linkTrackEvents="event53,event76",s.events=s.linkTrackEvents,wminst.trackLink(e.action))),s.clearVars()})),PubSub.subscribe("article-start",(function(e){wminst.trackArticleViewed(e)})),PubSub.subscribe("article-twentyfive",(function(e){wminst.trackArticleViewed(e)})),PubSub.subscribe("article-fifty",(function(e){wminst.trackArticleViewed(e)})),PubSub.subscribe("article-seventyfive",(function(e){wminst.trackArticleViewed(e)})),PubSub.subscribe("article-complete",(function(e){wminst.trackArticleViewed(e)})),PubSub.subscribe("user-account",(function(e){wminst.trackUserAccount(e)})),PubSub.subscribe("live-story-post",(function(e){wminst.trackLiveStoryPost(e)})),PubSub.subscribe("click-interaction",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,eVar36,prop59,eVar59,prop69,eVar69,prop73,eVar73,list2",s.linkTrackEvents="event76",s.events=s.linkTrackEvents,s.eVar36=wminst.Util.getCNNKruxID(),s.prop59=wminst.Util.getCNNAdobeID();try{s.prop69=e.interaction.toLowerCase(),-1!==s.prop69.indexOf("topics:")&&"topics:overlay:closed"!==s.prop69&&"topics:topics-tray-close"!==s.prop69&&"topics:topics-tray-expand"!==s.prop69&&(s.linkTrackVars=s.linkTrackVars+",prop4,eVar4,eVar105",wminst.Util.setPageAttribution())}catch(e){}try{wminst.trackLink(e.interaction.toLowerCase())}catch(e){}s.clearVars()})),PubSub.subscribe("sortpost-click",(function(e){s.manageVars("clearVars"),s.linkTrackVars="events,prop23,eVar23,eVar36,prop69,eVar69",s.linkTrackEvents="event76",s.events=s.linkTrackEvents;try{s.prop23=e.headline.toLowerCase()||wminst.Util.getCNNPageHeadline()}catch(e){s.prop23=wminst.Util.getCNNPageHeadline()}s.eVar36=wminst.Util.getCNNKruxID();try{s.prop69=e.interaction}catch(e){}try{var t=e.interaction;"string"==typeof t&&(t=t.replace(": "," ")),wminst.trackLink(t)}catch(e){}s.clearVars()})),wminst.subscribersReady=!0;
});</script><script data-anno-uid="anno-uid-p4j18hqktms">_satellite["_runScript11"](function(event, target, Promise) {
wminst.isLiveVid=!1,wminst.live_interval=0,wminst.setinterval_id=0,wminst.isAd=!1,wminst.adVidId="",wminst.adRange="",wminst.is_autoplay=!1,wminst.isLivePaused=!1,wminst.isTVEEpisodePaused=!1,wminst.is_preroll_occur=!1,wminst.trackLinkVideo=function(e,t){var i=["cnnvideo-autostart","cnnvideo-start","cnnvideo-live"].includes(e);wminst.Util.setCommonVars(i),wminst.Util.setVideoVars(t,i),s.tl(this,"o",e+":"+(t.title||t.headline||"").toLowerCase())},wminst.isTVEAuth=function(e){return""!==wminst.Util.getMVPD(e)||wminst.isFreePreview(e)||wminst.isEventBasedPreview(e)},wminst.isFreePreview=function(e){return"freeview"==wminst.Util.getPreviewType(e)||"temppass_cnn10min"==wminst.Util.getMVPD(e)},wminst.isEventBasedPreview=function(e){return"ebp"==wminst.Util.getPreviewType(e)||"eventpreview"==wminst.Util.getMVPD(e)},wminst.isFASTContent=function(e){return"fast"==wminst.getVCType4(e)||"livec76319f599742ab668c8b3ba6dcfed3ce7e817ad"==e.id||"livedbcedb554833b248c3ce8374acd2bbcd3983d7dd"==e.id},wminst.isNGTVContent=function(e){return void 0!==e.id&&-1!=e.id.indexOf("cvplive/cnngo")},wminst.isTVEContent=function(e){return wminst.Util.isTVEPage()||wminst.isTVEAuth(e)},wminst.isTVETrailer=function(e){return wminst.isTVEContent(e)&&("trailer"==e.video_type||"clip"==e.video_type)},wminst.isTVEEpisode=function(e){return wminst.isTVEContent(e)&&("episode"==e.video_type||"film"==e.video_type)},wminst.isTVELive=function(e){return wminst.isTVEContent(e)&&"live"==e.playerType},wminst.isVideoLive=function(e){return 1==e.isLive||"true"==e.isLive},wminst.isVideoAutoStarted=function(e){return!0===e.isAutoStart&&(!0===e.isAutostartSuccessful||!0===e.is_autoplay_allowed)},wminst.getVCType4=function(e){return(e.video_type||"").toLowerCase().replace("_","-")},wminst.startVideoProgressTimer=function(e){wminst.setinterval_id=setInterval((function(){window.trackVideoProgress(e)}),6e4)},wminst.stopVideoProgressTimer=function(){wminst.setinterval_id&&clearInterval(wminst.setinterval_id)},wminst.setVideoLinkTrackVars=function(){s.linkTrackVars="events,products,eVar1,eVar3,eVar4,eVar7,eVar8,eVar10,eVar14,eVar16,eVar20,eVar22,eVar23,eVar41,prop31,eVar31,eVar34,eVar36,eVar37,eVar42,prop43,prop44,prop46,eVar46,prop47,eVar47,eVar48,prop50,eVar52,eVar54,eVar56,eVar60,eVar64,eVar66,eVar67,eVar68,eVar70,eVar71,eVar72,prop73,eVar73,prop75,eVar75,eVar103,list2"},wminst.setVideoEVars=function(){wminst.Util.setEVars("1,3,4,7,8,10,14,16,20,23,31,34,37,41,52,54,56,60,64,66,68,70,71,72")},wminst.updateAutoStartType=function(){"string"==typeof s.prop70&&""!==s.prop70&&(s.prop70=s.prop70.replace("noautostart","autostart"))},wminst.updateVideoVars=function(){!0===wminst.is_autoplay&&wminst.updateAutoStartType(),wminst.setVideoEVars(),s.prop43||(s.prop50="")},wminst.setVideoPlayerType=function(e){var t="vod player",i=wminst.Util.getDataLayerV1();(i.video_player_type?t=i.video_player_type:(wminst.isVideoLive(e)||e.player_type&&"live"==(t=e.player_type))&&(t="live player"),wminst.Util.isFavePage())&&(-1!=window.location.pathname.indexOf("/v1/synacor")&&(t="synacor player"));s.prop1=t,s.eVar1="D=c1"},wminst.setPublishDate=function(e){var t=(e.dateCreated||{}).text||"",i=(e.lastModified||{}).text||"",n=""!=t?t.split("/"):"";""!=n&&4!=n[0].length&&(t="20"+n[2]+"/"+n[0]+"/"+n[1]),s.prop10=wminst.Util.getCNNDaysSinceLastPublish(t),s.eVar10="D=c10",s.prop16=t||i?t+"|"+i:"",s.eVar16="D=c16"},wminst.setBrandingSocial=function(){if(wminst.Util.isFavePage()){var e=window.location.pathname;-1!=e.indexOf("/v1/amp")&&(s.prop14="google amp"),-1!=e.indexOf("/v1/fav")&&(s.prop14="embed"),-1!=e.indexOf("/v1/synacor")&&(s.prop14="synacor player")}wminst.Util.isFBIAPage()&&(s.prop14=window.CNN.omniture.branding_social),s.prop14&&(s.eVar14="D=c14")},wminst.setVideoTitle=function(e){try{e.id;var t=(e.title||e.headline||"").toLowerCase(),i=(e.show_name||"").toLowerCase();wminst.isTVEContent(e)?s.prop29=(i?i+"|":"")+t:s.prop29=t,s.eVar41="D=c29"}catch(e){}},wminst.setAuthenticationState=function(e){s.prop34="does not require authentication",wminst.isTVEAuth(e)?s.prop34="requires authentication":e.auth_state&&(s.prop34=e.auth_state),s.eVar34="D=c34"},wminst.setContentTypeLevel2=function(e){var t="vod",i="non tve",n="clip",r=wminst.getVCType4(e)||"clip";s.prop1.includes("live")&&(t="live",i="requires authentication"==s.prop34?"tve":"non tve",n="live",r=wminst.isFASTContent(e)?"fast":"live"),(s.prop1.includes("tve")||wminst.isTVELive(e)||"tve"==e.auth_type)&&(t="live",i="tve",n="live",r="live"),wminst.isTVETrailer(e)?(t="vod",i="tve",n="clip",r="trailer"):wminst.isTVEEpisode(e)&&(t="vod",i="tve",n=e.video_type,r=e.video_type);var a=wminst.isAd?"ad":"content";s.prop54="video:"+t+":"+i+":"+n+":"+r+":"+a,s.eVar54="D=c54"},wminst.setNGTVVars=function(e){s.prop1="ngtv",s.eVar1="D=c1",s.prop2=e.author,s.eVar2="D=c2","live"!=e.content_type2&&"dvr"!=e.content_type2||(s.prop7=s.eVar7="");try{if(e.dateCreated){var t=wminst.Util.gCNNDaysSinceLastPublish(e.dateCreated);s.prop10=t+"",s.eVar10="D=c10",s.prop16=e.dateCreated,s.eVar16="D=c16"}}catch(e){}s.prop14=s.eVar14="",e.show_name=e.show_name||"",e.episode_title=e.episode_title||"",e.segment_name=e.segment_name||"","tve"==e.content_type1&&(e.title=e.show_name+":"+e.episode_title+":"+e.segment_name,e.live_stream_name&&"hln news"==e.live_stream_name&&(e.title="hln news"),s.prop29=e.title,s.prop32="video"),s.prop31=e.show_name,s.eVar31="D=c31",s.prop33="adbp:video start",s.eVar42=e.id,void 0!==e.isBreakingNews&&1==e.isBreakingNews&&(s.eVar43="ngtv:breaking_news"),e.segment_type&&(s.eVar43=e.segment_type),e.content_type1=e.content_type1||"",e.content_type2=e.content_type2||"",e.content_type3=e.content_type3||"",e.content_type4=e.content_type4||"",e.content_type5=wminst.isAd?"ad":"content",s.prop54="video:"+v.content_type2+":"+v.content_type1+":"+v.content_type3+":"+v.content_type4+":"+v.content_type5,e.content_type3&&"episode"!=e.content_type3&&(s.prop58=s.eVar58=""),s.prop60=s.eVar60="",s.prop61=s.eVar61="",s.prop64=s.eVar64="","non tve"==e.content_type1&&"vod"==e.content_type2&&"clip"==e.content_type3||(s.prop68=s.eVar68="",s.prop71=s.eVar71=""),s.prop70=autoStartType+":cnngo",s.eVar70="D=c70"},wminst.setVideoCommonData=function(e){s.manageVars("clearVars"),s.prop33="adbp:video start",e.video_player&&"undefined"!==e.video_player&&""!==e.video_player&&(s.prop52=e.video_player,s.eVar52="D=c52"),e.video_player&&-1!==e.video_player.indexOf("theo")&&(!0===e.isVr?(s.prop52="theo360",s.eVar52="D=c52",s.prop33="adbp:video:360"):(s.prop52=e.video_player,s.eVar52="D=c52")),s.prop37=wminst.Util.getCNNPlatform(),s.prop37&&""!=s.prop37&&(s.eVar37="D=c37"),void 0!==e.id&&""!=e.id&&-1!=e.id.indexOf("invalid-id-video-player")&&(s.prop43=wminst.Util.getCNNPostID(),s.prop50=wminst.Util.getCNNPostTitle()),s.list1=wminst.Util.getCEPTopisForVideo(e),s.prop72=e.free_preview||"",s.eVar72="D=c72",void 0!==e.video_focus&&(s.prop66=e.video_focus,s.eVar66="D=c66"),e.player_type&&""!=e.player_type&&("van"==e.player_type?(s.prop31="van",s.eVar31="D=c31",s.prop32="video",s.server=e.consumer||"",s.prop71=e.source.toLowerCase()||"",s.eVar71="D=c71"):"tve"!=e.player_type&&"live"!=e.player_type&&"live player"!=e.player_type||(s.prop3=e.category||"",s.eVar3="D=c3",s.prop31="van",s.eVar31="D=c31")),wminst.setVideoPlayerType(e);try{(window.location.href.indexOf("fave.api.cnn.io")>-1||window.location.href.indexOf("fave-api.cnn.com")>-1)&&e.video_player&&-1!==e.video_player.indexOf("theo")&&(s.prop32="content:video:nocollection",void 0!==window.CNN.omniture.template_type&&"live-story"==window.CNN.omniture.template_type&&(s.prop32="live story")),s.prop2=window.CNN.omniture.cap_author||"",s.eVar2="D=c2",s.prop3=e.category||"",s.eVar3="D=c3",s.prop7=e.trt||"",s.eVar7="D=c7"}catch(e){}s.prop8=wminst.Util.getCNNVisitNumber(28),wminst.setPublishDate(e),wminst.setBrandingSocial();try{if(wminst.Util.isFBIAPage()){var t=CNN.omniture.vpage_name;s.pageName=wminst.Util.getCNNPageName(t)}}catch(e){}s.eVar22=wminst.Util.getCNNVideoOpportunity(),wminst.setVideoTitle(e);try{s.prop31=(window.CNN.omniture.cap_show_name||"").toLowerCase(),s.eVar31="D=c31"}catch(e){}wminst.setAuthenticationState(e),s.eVar36||(s.eVar36=wminst.Util.getCNNKruxID()),s.eVar42=e.id,s.prop44||(s.prop44=wminst.Util.getCNNSourceID()),s.prop46=wminst.Util.getCNNTransactionID(),wminst.setContentTypeLevel2(e),s.prop56=wminst.Util.getCNNOrientation();try{if(e.dateAired){var i=wminst.Util.gCNNDaysSinceLastPublish(e.dateAired);s.prop58=i+"",s.eVar58="D=c58"}}catch(e){}var n=wminst.isVideoAutoStarted(e)?"autostart":"noautostart";try{window.CNN&&window.CNN.omniture&&"article"==window.CNN.omniture.cap_content_type?(s.prop70=n+":editorial",s.eVar70="D=c70"):!e.isLive||1!=e.isLive&&"true"!=e.isLive?(s.prop70=n+":vod",s.eVar70="D=c70"):(s.prop70=n+":live",s.eVar70="D=c70")}catch(e){}try{if(window.location.pathname.match(/video\/playlists\/./)){var r=/video\/playlists\/(.+)/.exec(window.location.pathname);s.prop60=r[1].replace(/\//g,""),s.eVar60="D=c60",s.prop70=n+":collection",s.eVar70="D=c70"}"player-one-tap-video"!=e.playerid&&(window.CNN.omniture.video_collection&&(s.prop60=window.CNN.omniture.video_collection,s.eVar60="D=c60",s.prop70=n+":collection",s.eVar70="D=c70"),window.video_collection&&(s.prop70=n+":collection:sunrise",s.eVar70="D=c70")),e.video_collection&&(s.prop60=e.video_collection,s.eVar60="D=c60",s.prop70=n+":collection",s.eVar70="D=c70"),""!=s.prop60&&void 0!==s.prop60||window.CNN.contentModel.analytics.pageTop.collectionHeadline&&(s.prop60=window.CNN.contentModel.analytics.pageTop.collectionHeadline,s.eVar60="D=c60"),""!==s.prop60&&(s.prop60=s.prop60.toLowerCase())}catch(e){}try{if(e.iscmsIIimport){var a="true"==e.iscmsIIimport?"secondary":"primary";s.prop61=a,s.eVar61="D=c61"}e.source&&(s.prop71=e.source.toLowerCase(),s.eVar71="D=c71")}catch(e){}try{e.ad_duration?(wminst.adRange=Math.round(e.ad_duration).toString(),s.prop68=wminst.adRange,s.eVar68="D=c68"):(s.prop68="no ad present",s.eVar68="D=c68")}catch(e){}try{wminst.isNGTVContent(e)||wminst.isTVEContent(e)?s.prop64="ngtv":s.prop64=wminst.Util.getCNNUIEngagement()}catch(e){}e.content_type2&&wminst.setNGTVVars(e),e.headline&&(s.prop23=e.headline.toLowerCase(),s.eVar23="D=c23"),s.list1=wminst.Util.getCEPTopisForVideo(e),s.eVar67=wminst.Util.getCNNPlayerState(e);try{window.CNN.omniture.gallery_name=""}catch(e){}try{window.CNN&&"undefined"!=window.CNN.omniture&&1==window.CNN.omniture.is_vision&&(s.prop71="cnn:vision",s.eVar71="D=c71")}catch(e){}try{wminst.Util.setPageAttribution(),s.prop46=wminst.Util.getCNNTransactionID(),s.prop47=wminst.Util.getCookie("ug"),s.eVar48=wminst.Util.getCNNTechStack(),s.prop26=wminst.Util.getCNNBaseURL(),s.prop75=wminst.Util.getCNNUserAuthState()}catch(e){}s.eVar103=e.auth_type||""},wminst.trackVideoStart=function(e){wminst.isAd=!1,wminst.isLiveVid=!1;var t,i=wminst.getVideoMetadata(e);wminst.setVideoCommonData(i),s.linkTrackVars="events,products,prop1,eVar1,prop3,eVar3,prop4,eVar4,prop7,eVar7,prop8,eVar8,prop10,eVar10,prop14,eVar14,prop16,eVar16,prop20,eVar20,eVar21,eVar22,prop23,eVar23,prop29,prop31,eVar31,prop34,eVar34,eVar36,prop37,eVar37,eVar41,eVar42,prop43,prop44,prop46,eVar46,prop47,eVar47,eVar48,prop49,eVar49,prop50,prop52,eVar52,prop54,eVar54,prop56,eVar56,prop60,eVar60,eVar61,prop64,eVar64,prop66,eVar66,eVar67,prop68,eVar68,prop70,eVar70,prop71,eVar71,prop72,eVar72,prop73,eVar73,prop75,eVar75,eVar103,eVar105,list2",wminst.isVideoAutoStarted(i)?(t="cnnvideo-autostart",s.linkTrackEvents="event32,event34",s.events="event32,event34",wminst.is_autoplay=!0,wminst.updateAutoStartType()):(t="cnnvideo-start",s.linkTrackEvents="event32",s.events="event32"),i.subcategory,i.subcategory&&""!=i.subcategory&&(s.linkTrackEvents="event23,"+s.linkTrackEvents,s.events=s.linkTrackEvents),void 0!==i.metas&&i.metas.branding&&""!=i.metas.branding&&(s.linkTrackEvents="event22,"+s.linkTrackEvents,s.events=s.linkTrackEvents),wminst.adVidId==i.id&&wminst.adRange>0&&(s.linkTrackEvents="event3,"+s.linkTrackEvents,s.events=s.linkTrackEvents,wminst.adVidId=""),s.prop7&&null!==s.prop7&&(s.linkTrackEvents=s.linkTrackEvents+",event85",s.events=s.linkTrackEvents,s.products=";;;;event85="+s.prop7),wminst.is_preroll_occur||(s.linkTrackEvents=s.linkTrackEvents+",event90",s.events=s.linkTrackEvents);var n=new wminst.getCNNMediaCollection;n.start(i.playerid,i.title?i.title:i.headline),s.prop4?s.eVar4="D=c4":s.eVar4="",s.eVar21=wminst.Util.getCNNVideoSequence(),s.prop72=s.eVar72="",s.prop31?s.prop31=s.prop31.toLowerCase():s.eVar31="",s.prop43||(s.prop50=""),s.eVar47="D=c47",s.eVar60=s.prop60,s.prop60="",s.prop64="",s.eVar64=wminst.Util.getCNNUIEngagement(),wminst.isTVEEpisode(i)&&(wminst.stopVideoProgressTimer(),wminst.startVideoProgressTimer(i)),wminst.trackLinkVideo(t,i),n.set(i.playerid,"vidStarted",!0),s.manageVars("clearVars")},wminst.trackVideoScrub=function(e){var t=wminst.getVideoMetadata(e),i=new wminst.getCNNMediaCollection;i.get(t.playerid,"hasScrubbed")||(i.set(t.playerid,"hasScrubbed",!0),wminst.setVideoCommonData(t),s.events="event119",wminst.setVideoLinkTrackVars(),s.linkTrackEvents=s.events,wminst.updateVideoVars(),wminst.trackLinkVideo("cnnvideo-scrub",t),s.manageVars("clearVars"))},wminst.trackVideoPause=function(e){var t=wminst.getVideoMetadata(e),i="true"==t.paused||1==t.paused,n=new wminst.getCNNMediaCollection,r=n.get(t.playerid,"isPaused");i!=r&&(n.pause(t.playerid),(1==wminst.isLiveVid||1==t.isLive||"true"==t.isLive||wminst.isTVEEpisode(t))&&(wminst.isLivePaused=wminst.isTVEEpisodePaused=i,wminst.stopVideoProgressTimer(),r&&wminst.startVideoProgressTimer(t))),wminst.setVideoCommonData(t);var a=i?"pause":"resume";s.events=i?"event55":"event56",wminst.setVideoLinkTrackVars(),s.linkTrackEvents=s.events,wminst.updateVideoVars(),wminst.trackLinkVideo("cnnvideo-"+a,t),s.manageVars("clearVars")},wminst.trackVideoMute=function(e){var t=wminst.getVideoMetadata(e);wminst.setVideoCommonData(t);var i=t.muted?"mute":"unmute";s.events=t.muted?"event111":"event112",wminst.setVideoLinkTrackVars(),s.linkTrackEvents=s.events,wminst.updateVideoVars(),wminst.trackLinkVideo("cnnvideo-"+i,t),s.manageVars("clearVars")},wminst.trackVideoMilestone=function(e,t){var i={10:["isTen","event40","cnnvideo-ten"],25:["isTwentyFive","event41","cnnvideo-twentyfive"],50:["isHalf","event2","cnnvideo-fifty"],75:["isSeventyFive","event42","cnnvideo-seventyfive"],90:["isNinety","event59","cnnvideo-ninety"]},n=i[t][0],r=i[t][1],a=i[t][2];wminst.isAd=!1;var o=wminst.getVideoMetadata(e);if(!wminst.isTVEEpisode(o)){var p=new wminst.getCNNMediaCollection;if(!p.get(o.playerid,n)&&!p.get(o.playerid,"hasScrubbed")){p.set(o.playerid,n,!0);var d=p.progress(o.playerid);wminst.setVideoCommonData(o),wminst.setVideoLinkTrackVars(),s.linkTrackEvents=r,s.events=r,s.products="",(d=wminst.capCNNTimeSpent(d,o.trt,wminst.live_interval))>0&&(s.linkTrackEvents=r+",event36",s.events=r+",event36",s.products=";;;;event36="+d),wminst.updateVideoVars(),wminst.trackLinkVideo(a,o),s.manageVars("clearVars")}}},wminst.trackVideoEnd=function(e,t){wminst.isAd=!1;var i=wminst.getVideoMetadata(e),n=new wminst.getCNNMediaCollection,r=n.complete(i.playerid);wminst.setVideoCommonData(i),wminst.setVideoLinkTrackVars();var a={complete:"event33",stop:"event110"}[t];s.linkTrackEvents=a,s.events=s.linkTrackEvents,s.products="",(r=wminst.capCNNTimeSpent(r,i.trt,wminst.live_interval))>0&&(s.linkTrackEvents=a+",event36",s.events=s.linkTrackEvents,s.products=";;;;event36="+r),wminst.updateVideoVars(),(wminst.isVideoLive(i)||wminst.isTVEEpisode(i))&&wminst.stopVideoProgressTimer(),wminst.trackLinkVideo("cnnvideo-"+t,i),n.set(i.playerid,"vidStarted",!1),n.set(i.playerid,"hasScrubbed",!1),n.set(i.playerid,"isPaused",!1),n.set(i.playerid,"isBuffering",!1),n.set(i.playerid,"isHalf",!1),n.set(i.playerid,"isTen",!1),n.set(i.playerid,"isTwentyFive",!1),n.set(i.playerid,"isSeventyFive",!1),n.set(i.playerid,"isNinety",!1),s.manageVars("clearVars")},PubSub.subscribe("cnnvideo-preroll",(function(e){wminst.isAd=!0;var t=wminst.getVideoMetadata(e);wminst.setVideoCommonData(t),wminst.adVidId=t.id,wminst.setVideoLinkTrackVars(),s.linkTrackEvents="event35",s.events="event35","string"==typeof t.adType&&"midroll"==t.adType.toLowerCase()&&(s.linkTrackEvents="event25",s.events="event25"),"string"==typeof t.adType&&"preroll"==t.adType.toLowerCase()&&(s.linkTrackEvents=s.linkTrackEvents+",event90",s.events=s.linkTrackEvents,wminst.is_preroll_occur=!0),"string"==typeof t.adType&&"postroll"==t.adType.toLowerCase()&&(s.linkTrackEvents="event82",s.events="event82"),(t.category&&"live"!==t.category||"true"!==t.isLive||!0!==t.isLive)&&(wminst.isLiveVid=!1),wminst.isVideoAutoStarted(t)&&(wminst.is_autoplay=!0,wminst.updateAutoStartType()),wminst.setVideoEVars(),s.prop43||(s.prop50=""),(wminst.isTVEEpisode(t)||1==wminst.isLiveVid||1==t.isLive||"true"==t.isLive)&&t.adType&&"midroll"==t.adType.toLowerCase()&&wminst.stopVideoProgressTimer(),wminst.trackLinkVideo("cnnvideo-"+t.adType.toLowerCase(),t);try{(t.content_type1&&"tve"==t.content_type1||wminst.isTVEEpisode(t)||wminst.isTVELive(t))&&wminst.startVideoProgressTimer(t)}catch(e){}s.manageVars("clearVars")})),PubSub.subscribe("cnnvideo-adcomplete",(function(e){var t=wminst.getVideoMetadata(e);wminst.setVideoCommonData(t),s.linkTrackVars="events,prop44",s.linkTrackEvents="event50",("midroll"==t.adType.toLowerCase()||1==wminst.isLiveVid&&"preroll"==t.adType.toLowerCase())&&(!t.player_type||"tve"!=t.player_type&&"live player"!=t.player_type&&"true"!=t.isLive||(s.prop33="adbp:none",wminst.trackLinkVideo("cnnvideo-adcomplete",t)),(wminst.isTVEEpisode(t)||wminst.isTVELive(t)||t.content_type1&&"tve"==t.content_type1||!0===t.isLive||"true"==t.isLive)&&(wminst.stopVideoProgressTimer(),wminst.startVideoProgressTimer(t))),wminst.isAd=!1,s.manageVars("clearVars")})),PubSub.subscribe("cnnvideo-midroll-complete",(function(e){var t=wminst.getVideoMetadata(e);wminst.setVideoCommonData(t),s.linkTrackVars="events,prop44",s.linkTrackEvents="event50",s.events="event50",("midroll"==t.adType.toLowerCase()||1==wminst.isLiveVid&&"preroll"==t.adType.toLowerCase())&&(!t.player_type||"tve"!=t.player_type&&"live player"!=t.player_type&&"true"!=t.isLive&&!0!==t.isLive||(s.prop33="adbp:none",wminst.trackLinkVideo("cnnvideo-adcomplete",t))),wminst.stopVideoProgressTimer(),wminst.startVideoProgressTimer(t),wminst.isAd=!1,s.manageVars("clearVars")})),PubSub.subscribe("cnnvideo-start",(function(e){wminst.trackVideoStart(e)})),PubSub.subscribe("cnnvideo-autostart",(function(e){wminst.trackVideoStart(e)})),PubSub.subscribe("cnnvideo-live",(function(e){wminst.isAd=!1,wminst.isLiveVid=!0,wminst.isLivePaused=!1;var t=wminst.getVideoMetadata(e);wminst.setVideoCommonData(t),s.linkTrackVars="events,prop1,eVar1,prop3,eVar3,prop4,eVar4,prop7,eVar7,prop8,eVar8,prop14,evar14,prop20,eVar20,evar21,eVar22,prop29,prop31,eVar31,prop34,eVar34,eVar36,prop37,eVar37,eVar41,eVar42,prop43,prop44,prop46,eVar46,prop47,eVar47,eVar48,prop50,prop52,eVar52,prop54,eVar54,prop56,eVar56,prop64,prop66,eVar66,eVar67,prop68,eVar68,prop70,eVar70,prop71,eVar71,prop72,eVar72,prop73,eVar73,prop75,eVar75,eVar103,eVar105,list2",s.linkTrackEvents="event1,event32",s.events="event1,event32";var i=new wminst.getCNNMediaCollection;if(i.start(t.playerid,t.title?t.title:t.headline),wminst.isVideoAutoStarted(t)&&(wminst.is_autoplay=!0,wminst.updateAutoStartType()),t.content_type2);else try{void 0!==t.isAutoStart&&1==t.isAutoStart&&(!0===t.isAutoplayAllowed&&!1!==isAutostartSuccessful||!0===t.is_autoplay_allowed&&!1!==t.is_autoplay_successful)&&(s.linkTrackEvents=s.linkTrackEvents+",event34",s.events=s.linkTrackEvents)}catch(e){}wminst.is_preroll_occur||(s.linkTrackEvents+=",event90",s.events=s.linkTrackEvents),wminst.isFASTContent(t)&&(s.linkTrackEvents+=",event109",s.events=s.linkTrackEvents),s.prop31?s.prop31=s.prop31.toLowerCase():s.eVar31="";try{if(void 0!==window.CNN.omniture.user_auth_state){var n=t.user_auth_state?t.user_auth_state:window.CNN.omniture.user_auth_state;s.prop75=n}else void 0===t.mvpd||"temppass_cnn10min"!=t.mvpd&&"TempPass_CNN10min"!=t.mvpd||(s.prop75="new_temppass_go")}catch(e){}void 0!==wminst.adVidId&&wminst.adVidId==t.id&&wminst.adRange>0&&(s.linkTrackEvents=s.linkTrackEvents+",event3",s.events=s.linkTrackEvents,wminst.adVidId=""),s.eVar23=s.prop23="",s.prop43||(s.prop50=""),wminst.isVideoLive(t)&&(wminst.stopVideoProgressTimer(),wminst.startVideoProgressTimer(t)),s.prop72=s.eVar72="",wminst.trackLinkVideo("cnnvideo-live",t),i.set(t.playerid,"vidStarted",!0),s.manageVars("clearVars")})),PubSub.subscribe("cnnvideo-episode",(function(e){wminst.isAd=!1;var t=wminst.getVideoMetadata(e);wminst.setVideoCommonData(t),s.linkTrackVars="events,list2",s.linkTrackEvents="event48",s.events="event48";var i=new wminst.getCNNMediaCollection;i.start(t.playerid,t.title?t.title:t.headline),wminst.trackLinkVideo("cnnvideo-episode",t),i.set(t.playerid,"vidStarted",!0),s.manageVars("clearVars")})),PubSub.subscribe("cnnvideo-autosegment",(function(e){wminst.isAd=!1;var t=wminst.getVideoMetadata(e);wminst.setVideoCommonData(t),s.linkTrackVars="events,list2",s.linkTrackEvents="event65";var i=new wminst.getCNNMediaCollection;i.start(t.playerid,t.title?t.title:t.headline),wminst.trackLinkVideo("cnnvideo-autosegment",t),i.set(t.playerid,"vidStarted",!0),s.manageVars("clearVars")})),PubSub.subscribe("cnnvideo-buffer",(function(e){var t=wminst.getVideoMetadata(e),i=void 0!==t.buffering&&t.buffering,s=new wminst.getCNNMediaCollection,n=s.get(t.playerid,"isBuffering");i!=n&&(s.buffer(t.playerid),(1==wminst.isLiveVid||1==t.isLive||"true"==t.isLive||wminst.isTVEEpisode(t))&&(wminst.stopVideoProgressTimer(),n&&wminst.startVideoProgressTimer(t)))})),PubSub.subscribe("cnnvideo-progress",(function(e){var t=wminst.getVideoMetadata(e);wminst.setVideoCommonData(t);var i=(new wminst.getCNNMediaCollection).progress(t.playerid);wminst.live_interval=60,i=wminst.capCNNTimeSpent(i,t.trt,wminst.live_interval),wminst.setVideoLinkTrackVars(),s.linkTrackEvents="event36",s.events="event36",wminst.updateVideoVars(),s.products=";;;;"+s.events+"="+i,60!=i||wminst.isLivePaused&&wminst.isTVEEpisodePaused||wminst.trackLinkVideo("cnnvideo-progress",t),s.manageVars("clearVars")})),PubSub.subscribe("cnnvideo-scrub",(function(e){wminst.trackVideoScrub(e)})),PubSub.subscribe("cnnvideo-pause",(function(e){wminst.trackVideoPause(e)})),PubSub.subscribe("cnnvideo-mute",(function(e){wminst.trackVideoMute(e)})),PubSub.subscribe("cnnvideo-ten",(function(e){wminst.trackVideoMilestone(e,10)})),PubSub.subscribe("cnnvideo-twentyfive",(function(e){wminst.trackVideoMilestone(e,25)})),PubSub.subscribe("cnnvideo-fifty",(function(e){wminst.trackVideoMilestone(e,50)})),PubSub.subscribe("cnnvideo-seventyfive",(function(e){wminst.trackVideoMilestone(e,75)})),PubSub.subscribe("cnnvideo-ninety",(function(e){wminst.trackVideoMilestone(e,90)})),PubSub.subscribe("cnnvideo-stop",(function(e){wminst.trackVideoEnd(e,"stop")})),PubSub.subscribe("cnnvideo-complete",(function(e){wminst.trackVideoEnd(e,"complete")}));try{let e=function(e){return"span."+e+"-container__back-player-icon-container"},t=e("player")+","+e("fave-player");document.querySelector(t).addEventListener("click",(function(){wminst.Util.log("Back button was clicked. Stop video progress."),wminst.stopVideoProgressTimer()}))}catch(e){}
});</script><script data-anno-uid="anno-uid-x46efhud46">_satellite["_runScript12"](function(event, target, Promise) {
wminst.isAudioInitiated=!1,wminst.setAudioInterval_id=0,wminst.liveAudioInterval=0,wminst.trackLinkAudio=function(e,t){wminst.Util.setUserAuthState(),wminst.Util.setIds(),s.tl(this,"o",e+": "+t.title.toLowerCase())},wminst.startAudioProgressTimer=function(e){wminst.setAudioInterval_id=setInterval((function(){window.trackAudioProgress(e)}),6e4)},wminst.stopAudioProgressTimer=function(){wminst.setAudioInterval_id&&clearInterval(wminst.setAudioInterval_id)},wminst.audioCommonData=function(e){var t,r,a="audio";try{r="aod",void 0===(t=e||{}).isLive||!t.isLive&&"true"!=t.isLive||(r="live"),s.trackingServer=wminst.Util.getSiteSpecificSettings(3),s.trackingServerSecure=wminst.Util.getSiteSpecificSettings(4),s.account=_satellite.getVar("RSID"),s.prop1=t.type,t.author&&""!==t.author&&(s.prop2=t.author.toLowerCase()),s.prop7=t.length+"",s.eVar7="D=c7",t.title&&""!==t.title&&(s.prop29=t.title.toLowerCase(),s.eVar41="D=c29"),s.eVar33="adbp:audio",s.prop33="",s.prop35=wminst.Util.getCodeVersion(),s.eVar42=t.id,s.eVar45=t.playlist_position+"",s.prop45="",s.eVar54=a+"|"+r+"|"+t.type,s.prop54="",s.eVar67=t.state+"|"+(t.status?t.status:"no value set")+"|"+(t.position?t.position:"inline"),s.prop67="",s.eVar82=t.rate+"",s.prop82=""}catch(e){}},PubSub.subscribe("audio-preroll",(function(e){s.manageVars("clearVars");var t=wminst.getAudioMetadata(e);s.linkTrackVars="events,prop1,eVar1,prop2,eVar2,prop7,eVar7,prop29,eVar33,prop35,eVar35,eVar41,eVar42,eVar45,eVar54,eVar67,eVar82",s.events="event91,event92",s.linkTrackEvents=s.events,wminst.isAudioInitiated=!0,wminst.audioCommonData(t),wminst.trackLinkAudio("audio-preroll",t),wminst.startAudioProgressTimer(t),s.clearVars()})),PubSub.subscribe("audio-start",(function(e){s.manageVars("clearVars");var t=wminst.getAudioMetadata(e),r=new wminst.getCNNMediaCollection;r.start(t.playerid,t.title),s.linkTrackVars="events,products,prop1,eVar1,prop2,eVar2,prop7,eVar7,prop29,eVar33,prop35,eVar35,eVar41,eVar42,eVar45,eVar54,eVar67,eVar82",s.events="event11",wminst.audioCommonData(t),wminst.isAudioInitiated||(s.events+=",event92"),s.prop7&&null!==s.prop7&&(s.events=s.events+",event64",s.products=";;;;event64="+s.prop7),s.linkTrackEvents=s.events,wminst.trackLinkAudio("audio-start",t),wminst.isAudioInitiated=!1,r.set(t.playerid,"audStarted",!0),wminst.stopAudioProgressTimer(),wminst.startAudioProgressTimer(t),s.clearVars()})),PubSub.subscribe("audio-autostart",(function(e){s.manageVars("clearVars");var t=wminst.getAudioMetadata(e),r=new wminst.getCNNMediaCollection;r.start(t.playerid,t.title),s.linkTrackVars="events,products,prop1,eVar1,prop2,eVar2,prop7,eVar7,prop29,eVar33,prop35,eVar35,eVar41,eVar42,eVar45,eVar54,eVar67,eVar82",s.events="event11",wminst.audioCommonData(t),wminst.isAudioInitiated||(s.events+=",event92"),s.prop7&&null!==s.prop7&&(s.events=s.events+",event64",s.products=";;;;event64="+s.prop7),s.linkTrackEvents=s.events,wminst.trackLinkAudio("audio-autostart",t),wminst.isAudioInitiated=!1,r.set(t.playerid,"audStarted",!0),wminst.stopAudioProgressTimer(),wminst.startAudioProgressTimer(t),s.clearVars()})),PubSub.subscribe("audio-complete",(function(e){s.manageVars("clearVars");var t=wminst.getAudioMetadata(e),r=new wminst.getCNNMediaCollection,a=r.complete(t.playerid);s.linkTrackVars="events,products,prop1,eVar1,prop2,eVar2,prop7,eVar7,prop29,eVar33,prop35,eVar35,eVar41,eVar42,eVar45,eVar54,eVar67,eVar82",s.linkTrackEvents="event97,event98",s.events=s.linkTrackEvents,wminst.audioCommonData(t),a>0&&(s.products=";;;;event98="+a),wminst.stopAudioProgressTimer(),wminst.trackLinkAudio("audio-complete",t),r.set(t.playerid,"audStarted",!1),r.set(t.playerid,"hasScrubbed",!1),r.set(t.playerid,"isPaused",!1),r.set(t.playerid,"isBuffering",!1),r.set(t.playerid,"isHalf",!1),r.set(t.playerid,"isTen",!1),r.set(t.playerid,"isTwentyFive",!1),r.set(t.playerid,"isSeventyFive",!1),s.clearVars()})),PubSub.subscribe("audio-pause",(function(e){var t=wminst.getAudioMetadata(e),r=void 0!==t.pause&&t.pause,a=new wminst.getCNNMediaCollection;a.get(t.playerid,"audStarted")&&(s.manageVars("clearVars"),s.linkTrackVars="events,prop1,eVar1,prop2,eVar2,prop7,eVar7,prop29,eVar33,prop35,eVar35,eVar41,eVar42,eVar45,eVar54,eVar67,eVar82",s.events="event100",r&&(s.events="event99"),s.linkTrackEvents=s.events,wminst.audioCommonData(t),wminst.trackLinkAudio(r?"audio-pause":"audio-resume",t));var i=a.get(t.playerid,"isPaused");r!=i&&(a.pause(t.playerid),wminst.stopAudioProgressTimer(),i&&wminst.startAudioProgressTimer(t)),s.manageVars("clearVars")})),PubSub.subscribe("audio-buffer",(function(e){var t=wminst.getAudioMetadata(e),s=void 0!==t.buffering&&t.buffering,r=new wminst.getCNNMediaCollection,a=r.get(t.playerid,"isBuffering");s!=a&&(r.buffer(t.playerid),wminst.stopAudioProgressTimer(),a&&wminst.startAudioProgressTimer(t))})),PubSub.subscribe("audio-scrub",(function(e){var t=wminst.getAudioMetadata(e);(new wminst.getCNNMediaCollection).set(t.playerid,"hasScrubbed",!0)})),PubSub.subscribe("audio-progress",(function(e){var t=wminst.getAudioMetadata(e),r=new wminst.getCNNMediaCollection;s.linkTrackVars="events,products,prop1,eVar1,prop2,eVar2,prop7,eVar7,prop29,eVar33,prop35,eVar35,eVar41,eVar42,eVar45,eVar54,eVar67,eVar82",s.events="event98",s.linkTrackEvents=s.events,wminst.audioCommonData(t);var a=r.progress(t.playerid);a>60&&(wminst.liveAudioInterval=60),(a=wminst.capCNNTimeSpent(a,t.length,wminst.liveAudioInterval))>0&&(s.products=";;;;event98="+a),60==a&&wminst.trackLinkAudio("audio-progress",t),s.manageVars("clearVars")}));
});</script><script data-anno-uid="anno-uid-6615ftn0xzw">_satellite["_runScript13"](function(event, target, Promise) {
wminst.Util.loadScript("//www.i.cdn.cnn.com/zion/zion-mb.min.js",(function(){try{if("undefined"!=typeof s){var i=ZionMessageBus.getInstance(),e=s.visitor.getMarketingCloudVisitorID(),n=s.visitor.getAnalyticsVisitorID();i.publish("id_found",{type:"adobe_ecid",value:e}),i.publish("id_found",{type:"adobe_vi",value:n})}}catch(i){console.error(i)}}));
});</script><iframe data-anno-uid="anno-uid-s9kz8jbpth" name="goog_topics_frame" src="https://securepubads.g.doubleclick.net/static/topics/topics_frame.html" style="display: none;"></iframe></body></html>
"""

print("🔍 开始内容提取...")
start_time = time.time()

try:
    result = extractor.extract(test_html)
    end_time = time.time()

    print(f"⏱️ 提取耗时: {end_time - start_time:.2f}秒\n")

    # 显示提取结果
    if result.success:
        print("✅ 内容提取成功！\n")

        print("📄 提取的主要内容:")
        print("=" * 50)
        print(result.content[:500] + "..." if len(result.content) > 500 else result.content)
        print("=" * 50)

        print(f"\n📊 提取统计:")
        print(f"  • 内容长度: {len(result.content)} 字符")
        print(f"  • 标题: {result.title}")
        print(f"  • 语言: {result.language}")
        print(f"  • 提取时间: {result.extraction_time:.3f}秒")

        if result.content_list:
            print(f"  • 结构化内容块: {len(result.content_list)}个")
            for i, item in enumerate(result.content_list[:3]):  # 显示前3个
                print(f"    [{i + 1}] {item.get('type', 'unknown')}: {item.get('content', '')[:50]}...")
    else:
        print("❌ 内容提取失败")
        print(f"错误信息: {result.error_message}")
        if result.error_traceback:
            print(f"错误详情:\n{result.error_traceback}")

except Exception as e:
    print(f"❌ 提取过程中发生异常: {e}")