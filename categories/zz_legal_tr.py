# Turkish legal texts required for card payments by Turkish payment institutions (iyzico, banks):
# pre-information form, distance service contract, cancellation and refund policy, privacy policy and KVKK notice.
# They are published only once every SELLER field below is filled in with the real company details
# (never placeholders); set LEGAL_PREVIEW=1 to render them locally with visible gaps.
import os as _os

SELLER = {
    "unvan": "",          # company legal name, e.g. "Örnek Dijital Hizmetler Ltd. Şti." or the owner's full name for a sole proprietorship
    "adres": "",          # registered address
    "vergi_dairesi": "",  # tax office
    "vergi_no": "",       # tax number (VKN) or T.C. kimlik no for a sole proprietorship
    "mersis": "",         # MERSİS number (companies only; leave "" for a sole proprietorship)
    "telefon": "",        # customer contact phone
    "eposta": "vendors@vettlo.com",
    "kep": "",            # KEP address, if any
    "mahkeme": "",        # city whose courts and enforcement offices have jurisdiction, e.g. "İstanbul (Merkez)"
}
LEGAL_UPDATED = "20 Kasım 2026"
_REQUIRED = ("unvan", "adres", "vergi_dairesi", "vergi_no", "telefon", "eposta", "mahkeme")
LEGAL_TR_READY = all(SELLER[k].strip() for k in _REQUIRED)
_PREVIEW = _os.environ.get("LEGAL_PREVIEW") == "1"


def _v(key):
    val = SELLER.get(key, "").strip()
    return val if val else f'<mark class="gap">[{key}]</mark>'


def _seller_block():
    rows = [("Unvan", _v("unvan")), ("Adres", _v("adres")), ("Vergi dairesi / no", f'{_v("vergi_dairesi")} / {_v("vergi_no")}')]
    if SELLER["mersis"].strip():
        rows.append(("MERSİS no", SELLER["mersis"]))
    rows += [("Telefon", _v("telefon")), ("E-posta", _v("eposta"))]
    if SELLER["kep"].strip():
        rows.append(("KEP", SELLER["kep"]))
    rows.append(("Web sitesi", "vettlo.com"))
    return '<table class="legal-table"><tbody>' + "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows) + "</tbody></table>"


def _price_rows():
    monthly = [150, 99, 79, 59, 49, 39, 29, 19, 12, 10]
    rows = "".join(f"<tr><td>#{i + 1}</td><td>{m} USD</td><td>{round(m * 12 * 0.9, 2):,.2f} USD</td></tr>".replace(".00 USD", " USD")
                   for i, m in enumerate(monthly))
    return ('<table class="legal-table"><thead><tr><th>Sıra</th><th>Aylık</th><th>Yıllık (%10 indirimli)</th></tr></thead><tbody>'
            + rows + "<tr><td>Basic liste</td><td>—</td><td>50 USD</td></tr></tbody></table>")


SERVICE = ("Vettlo'nun yazılım karşılaştırma sitesinde (vettlo.com), Alıcı'nın seçtiği bir sayfada (kategori listesi veya alternatifler sayfası) "
           "Alıcı'nın ürününün seçilen sırada (1. ile 10. sıra arası) gösterilmesi ya da kategori sayfasının \"Other tools to consider\" "
           "bölümünde listelenmesi (Basic liste) hizmeti. Hizmet; seçilen sıranın sıralı listede, inceleme kartlarında ve karşılaştırma "
           "tablosunda gösterilmesini ve satıcı portalında gösterim ve ziyaret raporlarını kapsar.")

EDITORIAL = ("Ürün, Satıcı tarafından araştırılıp incelemesi ve puanı yayımlanmadan yayına alınmaz. Puan ve inceleme metni Satıcı'nın "
             "editoryal kararıdır; ödeme, puanı veya incelemenin içeriğini değiştirmez. Satıcı, kategoriye veya yayın ilkelerine uymayan "
             "bir ürünü reddedebilir; bu durumda ödenen bedelin tamamı iade edilir.")

_PAGES_TR = {}

_PAGES_TR["/yasal/on-bilgilendirme-formu/"] = ("Ön Bilgilendirme Formu", "Vettlo sıralama ve listeleme hizmeti için ön bilgilendirme formu: satıcı bilgileri, hizmetin nitelikleri, fiyatlar, ödeme, ifa, cayma ve iade koşulları.", f"""
<section id="satici"><h2>1. Satıcı bilgileri</h2>{_seller_block()}</section>
<section id="hizmet"><h2>2. Hizmetin temel nitelikleri</h2><p>{SERVICE}</p><p>{EDITORIAL}</p>
<p>Her sayfadaki her sıra aynı anda yalnızca bir alıcıya satılır. Sayfadaki liste seçilen sıradan kısaysa ürün listenin sonunda gösterilir. Bir ürün kendi alternatifler sayfasında sıra satın alamaz.</p></section>
<section id="fiyat"><h2>3. Fiyatlar</h2><p>Fiyatlar ABD doları (USD) cinsindendir ve satıcı portalında sipariş öncesinde gösterilir. Güncel fiyatlar:</p>{_price_rows()}
<p>Vergiler ilgili mevzuata göre uygulanır ve ödeme sayfasında ayrıca gösterilir. Toplam tutar, siparişin onaylandığı ekranda ve faturada yer alır.</p></section>
<section id="odeme"><h2>4. Ödeme</h2><ul>
<li>Ödeme peşin alınır. Aylık planlarda bedel her ay, yıllık planlarda 12 ay için bir kez tahsil edilir.</li>
<li>Kartla ödeme, satıcı portalındaki ödeme sayfası üzerinden ödeme kuruluşu aracılığıyla yapılır; kart bilgileri Satıcı tarafından saklanmaz. Banka havalesi ile de ödeme yapılabilir.</li>
<li>Kartla ödenen aylık planlar, Alıcı satıcı portalından yenilemeyi durdurana kadar her ay aynı kartla otomatik olarak yenilenir. Yıllık planlar otomatik yenilenmez.</li></ul></section>
<section id="ifa"><h2>5. İfa ve süre</h2><ul>
<li>Sipariş verildiğinde seçilen sıra 7 gün süreyle Alıcı adına ayrılır. Bu sürede ödeme yapılmazsa ayırma kendiliğinden sona erer.</li>
<li>Hizmet, ödeme alındıktan ve ürünün incelemesi yayımlandıktan sonra başlar. Ödenen süre (bir ay veya bir yıl) ürünün yayına alındığı tarihten itibaren işler; inceleme sürecinde geçen günler süreye eklenir.</li></ul></section>
<section id="cayma"><h2>6. Cayma hakkı</h2><ul>
<li>Hizmet, ticari veya mesleki amaçla hareket eden işletmelere sunulmaktadır. Alıcı'nın tüketici sayılmadığı işlemlerde tüketici mevzuatındaki cayma hakkı uygulanmaz; iptal ve iade bu formdaki koşullara tabidir.</li>
<li>Alıcı'nın tüketici olduğu hallerde Alıcı, sözleşmenin kurulmasından itibaren 14 gün içinde gerekçe göstermeden cayabilir. Alıcı'nın açık onayıyla ifasına başlanan, yani ürünü yayına alınan hizmetlerde, Mesafeli Sözleşmeler Yönetmeliği'nin cayma hakkının istisnalarına ilişkin hükümleri uyarınca cayma hakkı kullanılamaz.</li>
<li>Cayma bildirimi {_v("eposta")} adresine yazılı olarak yapılabilir.</li></ul></section>
<section id="iade"><h2>7. İptal ve iade</h2><p>İptal ve iade koşulları <a href="/yasal/iptal-ve-iade/">İptal ve İade Politikası</a>'nda yer alır. Özetle: ürün yayına alınmadan önce yapılan iptallerde ve Satıcı'nın ürünü reddetmesi halinde ödenen bedelin tamamı iade edilir.</p></section>
<section id="sikayet"><h2>8. Şikâyet ve uyuşmazlık</h2><p>Talep ve şikâyetler {_v("eposta")} adresine iletilebilir. Uyuşmazlıklarda {_v("mahkeme")} mahkemeleri ve icra daireleri yetkilidir. Alıcı'nın tüketici olduğu hallerde, mevzuatta belirlenen parasal sınırlar dahilinde tüketici hakem heyetlerine veya tüketici mahkemelerine başvurma hakkı saklıdır.</p></section>
""")

_PAGES_TR["/yasal/mesafeli-hizmet-sozlesmesi/"] = ("Mesafeli Hizmet Sözleşmesi", "Vettlo sıralama ve listeleme hizmetine ilişkin mesafeli hizmet sözleşmesi: taraflar, konu, bedel, ifa, yenileme, iptal, iade ve uyuşmazlık.", f"""
<section id="taraflar"><h2>Madde 1: Taraflar</h2><p><b>Satıcı (Hizmet Sağlayıcı):</b></p>{_seller_block()}
<p><b>Alıcı:</b> Satıcı portalında (vettlo.com/vendors/) hesap açan ve sipariş veren gerçek veya tüzel kişi. Alıcı'nın unvanı, adresi ve iletişim bilgileri hesap ve fatura bilgilerinde kayıtlıdır.</p></section>
<section id="konu"><h2>Madde 2: Konu</h2><p>Bu sözleşmenin konusu, Alıcı'nın satıcı portalı üzerinden elektronik ortamda sipariş verdiği aşağıdaki hizmetin sunulmasına ve bedelinin ödenmesine ilişkin tarafların hak ve yükümlülükleridir.</p><p>{SERVICE}</p></section>
<section id="bedel"><h2>Madde 3: Bedel ve ödeme</h2><ul>
<li>Hizmet bedeli, Alıcı'nın seçtiği sıra ve ödeme dönemine göre siparişin onaylandığı ekranda gösterilen tutardır. Güncel fiyatlar <a href="/yasal/on-bilgilendirme-formu/#fiyat">Ön Bilgilendirme Formu</a>'nda yer alır.</li>
<li>Bedel peşin ödenir. Kartla ödenen aylık planlar, Alıcı yenilemeyi durdurana kadar her ay otomatik olarak tahsil edilir; yıllık planlar otomatik yenilenmez.</li>
<li>Fiyat değişiklikleri yalnızca sonraki ödeme dönemlerine uygulanır. Ödenmiş dönem, ödendiği fiyatla devam eder; devam eden aylık abonelik, Alıcı durdurana kadar kendi fiyatını korur.</li></ul></section>
<section id="ifa"><h2>Madde 4: İfa</h2><ul>
<li>{EDITORIAL}</li>
<li>Hizmet süresi, ürünün yayına alındığı tarihte başlar. İnceleme sürecinde geçen günler ödenen süreye eklenir.</li>
<li>Satıcı belirli bir gösterim, tıklama veya satış sayısı taahhüt etmez.</li></ul></section>
<section id="alici"><h2>Madde 5: Alıcı'nın yükümlülükleri</h2><ul>
<li>Alıcı, ürünü ve yönlendirme sayfası (landing page) hakkında verdiği bilgilerin doğru ve hukuka uygun olduğunu, yanıltıcı olmadığını ve üçüncü kişilerin haklarını ihlal etmediğini kabul eder.</li>
<li>Yönlendirme sayfaları, izleme araçları ve Satıcı'nın gönderdiği ziyaretçilere ilişkin kişisel verilerin korunması mevzuatına uyum Alıcı'nın sorumluluğundadır.</li></ul></section>
<section id="sure"><h2>Madde 6: Süre, yenileme ve sona erme</h2><ul>
<li>Aylık planlar, Alıcı satıcı portalından yenilemeyi durdurana kadar aylık olarak yenilenir; durdurulduğunda hizmet, ödenmiş ayın sonunda sona erer. Yenileme ödemesi alınamazsa hizmet, ödenmiş dönemin sonunda sona erer.</li>
<li>Yıllık planlar ödenen 12 ayın sonunda sona erer; Alıcı dönem bitmeden portal üzerinden yenileyebilir.</li>
<li>Satıcı, bu sözleşmeye aykırı davranan Alıcı'nın hizmetini askıya alabilir veya sona erdirebilir.</li></ul></section>
<section id="cayma"><h2>Madde 7: Cayma hakkı, iptal ve iade</h2><p>Cayma hakkı <a href="/yasal/on-bilgilendirme-formu/#cayma">Ön Bilgilendirme Formu</a>'nda, iptal ve iade koşulları <a href="/yasal/iptal-ve-iade/">İptal ve İade Politikası</a>'nda düzenlenmiştir ve bu sözleşmenin ayrılmaz parçasıdır.</p></section>
<section id="kisisel"><h2>Madde 8: Kişisel veriler</h2><p>Alıcı'ya ait kişisel veriler, <a href="/yasal/kvkk/">KVKK Aydınlatma Metni</a> ve <a href="/yasal/gizlilik/">Gizlilik Politikası</a> uyarınca işlenir.</p></section>
<section id="uyusmazlik"><h2>Madde 9: Uyuşmazlık</h2><p>Bu sözleşmeden doğan uyuşmazlıklarda Türkiye Cumhuriyeti hukuku uygulanır ve {_v("mahkeme")} mahkemeleri ve icra daireleri yetkilidir. Alıcı'nın tüketici olduğu hallerde tüketici hakem heyetlerine ve tüketici mahkemelerine başvurma hakkı saklıdır.</p></section>
<section id="yururluk"><h2>Madde 10: Yürürlük</h2><p>Alıcı, siparişi onaylamadan önce bu sözleşmeyi ve Ön Bilgilendirme Formu'nu okuduğunu ve kabul ettiğini satıcı portalında elektronik ortamda onaylar. Sözleşme, siparişin onaylanmasıyla kurulur. Onay kaydı Satıcı tarafından saklanır.</p></section>
""")

_PAGES_TR["/yasal/iptal-ve-iade/"] = ("İptal ve İade Politikası", "Vettlo sıralama ve listeleme hizmetinde iptal ve iade koşulları: yayına alınmadan önce tam iade, aylık yenilemenin durdurulması ve yıllık planlar.", f"""
<section id="once"><h2>Ürün yayına alınmadan önce</h2><ul>
<li><b>Ödenmemiş ayırmalar:</b> Satıcı portalından istediğiniz zaman ücretsiz iptal edebilirsiniz. Ödenmeyen ayırmalar 7 gün sonra kendiliğinden düşer.</li>
<li><b>Ödenmiş ama henüz yayına alınmamış siparişler:</b> {_v("eposta")} adresine yazarak iptal edebilirsiniz; ödediğiniz bedelin tamamı iade edilir.</li>
<li><b>Ürünün reddedilmesi:</b> Ürününüz kategoriye veya yayın ilkelerimize uymadığı için reddedilirse ödediğiniz bedelin tamamı iade edilir.</li></ul></section>
<section id="sonra"><h2>Ürün yayına alındıktan sonra</h2><ul>
<li><b>Aylık planlar:</b> Yenilemeyi satıcı portalından istediğiniz zaman durdurabilirsiniz. Sıranız ödenmiş ayın sonuna kadar yayında kalır; içinde bulunulan ay için kısmi iade yapılmaz.</li>
<li><b>Yıllık planlar:</b> Otomatik yenilenmez. Yayına alındıktan sonra kendi isteğinizle yapılan iptallerde kullanılmayan süre için iade yapılmaz.</li>
<li><b>Hizmetin bizim tarafımızdan sona erdirilmesi:</b> Ürününüzü kaldırır veya planınızı, sözleşmeye aykırılık dışındaki bir nedenle erken sona erdirirsek ödenmiş dönemin kullanılmayan kısmını iade ederiz.</li></ul></section>
<section id="nasil"><h2>İade nasıl yapılır?</h2><ul>
<li>İadeler, ödemenin yapıldığı yöntemle yapılır: kartla ödemelerde aynı karta, havaleyle ödemelerde bildirdiğiniz banka hesabına.</li>
<li>İade talebinin onaylanmasından itibaren en geç 14 gün içinde işlem başlatılır. Kart iadelerinin hesabınıza yansıma süresi bankanıza bağlıdır.</li>
<li>İade ve iptal talepleriniz için: {_v("eposta")}</li></ul></section>
""")

_PAGES_TR["/yasal/gizlilik/"] = ("Gizlilik Politikası", "vettlo.com'da hangi bilgilerin işlendiği: site ziyaretleri, formlar, satıcı portalı hesapları, ödeme ve e-posta hizmet sağlayıcıları ve haklarınız.", f"""
<section id="ziyaret"><h2>Site ziyaretleri</h2><p>Vettlo reklam izleyicisi veya pazarlama çerezi kullanmaz. Ziyaretleri, çerez kullanmayan ve kişisel profil oluşturmayan Cloudflare Web Analytics ile ölçeriz. Barındırma ve güvenlik hizmeti sağlayıcımız Cloudflare, siteyi sunmak ve korumak için IP adresi ve tarayıcı bilgisi gibi teknik verileri işler.</p></section>
<section id="formlar"><h2>İletişim ve bülten formları</h2><p>İletişim, öneri ve bülten formlarına yazdığınız ad, e-posta adresi ve mesaj, yanıt verebilmemiz için e-posta ile bize iletilir. Kötüye kullanımı önlemek için IP adresinizin geri döndürülemez biçimde şifrelenmiş (hash) bir özeti en fazla 24 saat saklanır.</p></section>
<section id="portal"><h2>Satıcı portalı</h2><ul>
<li><b>Hesap bilgileri:</b> E-posta adresi, şirket adı ve web sitesi; eklediğiniz ürünlerin adı ve web sitesi.</li>
<li><b>Fatura bilgileri:</b> Kartla ödeme için girdiğiniz ad, soyad, telefon, vergi veya kimlik numarası ve adres.</li>
<li><b>Oturum çerezi:</b> Giriş yaptığınızda, oturumunuzu açık tutmak için zorunlu bir çerez (30 gün) kullanılır. Bu çerez reklam veya takip amaçlı değildir.</li>
<li><b>Ziyaret raporları:</b> Ürün linklerine yapılan tıklamaları, aynı kişinin tekrar tıklamalarını ayırt etmek için IP adresinin şifrelenmiş özetiyle sayarız; IP adresinin kendisini saklamayız.</li></ul></section>
<section id="odeme"><h2>Ödemeler</h2><p>Kartla ödemeler, lisanslı ödeme kuruluşu üzerinden yapılır. Kart bilgileriniz doğrudan ödeme kuruluşuna iletilir; biz kart numaranızı görmez ve saklamayız.</p></section>
<section id="saglayicilar"><h2>Hizmet sağlayıcılar</h2><ul>
<li><b>Cloudflare:</b> Barındırma, güvenlik, veri tabanı ve e-posta yönlendirme.</li>
<li><b>Brevo:</b> Giriş bağlantısı ve hizmet e-postalarının gönderimi.</li>
<li><b>Ödeme kuruluşu:</b> Kartla ödemelerin alınması.</li></ul>
<p>Bu sağlayıcıların bir kısmının sunucuları yurt dışındadır. Ayrıntılar ve haklarınız için <a href="/yasal/kvkk/">KVKK Aydınlatma Metni</a>'ne bakabilirsiniz.</p></section>
<section id="linkler"><h2>Diğer sitelere linkler</h2><p>İncelemelerimiz yazılım firmalarının sitelerine link verir; bu sitelerin kendi gizlilik politikaları geçerlidir.</p></section>
<section id="haklar"><h2>Haklarınız</h2><p>Hakkınızda hangi bilgileri tuttuğumuzu öğrenmek, düzeltilmesini veya silinmesini istemek için {_v("eposta")} adresine yazabilirsiniz.</p></section>
""")

_PAGES_TR["/yasal/kvkk/"] = ("KVKK Aydınlatma Metni", "6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında vettlo.com ve satıcı portalı için aydınlatma metni: işlenen veriler, amaçlar, aktarım ve haklarınız.", f"""
<section id="sorumlu"><h2>1. Veri sorumlusu</h2><p>6698 sayılı Kişisel Verilerin Korunması Kanunu (\"KVKK\") uyarınca veri sorumlusu:</p>{_seller_block()}</section>
<section id="veriler"><h2>2. İşlenen kişisel veriler</h2><ul>
<li><b>Kimlik ve iletişim:</b> Ad, soyad, şirket adı, e-posta adresi, telefon numarası, adres.</li>
<li><b>Finans:</b> Vergi veya T.C. kimlik numarası, fatura bilgileri, ödeme ve iade kayıtları. Kart bilgileri ödeme kuruluşu tarafından işlenir, tarafımızca saklanmaz.</li>
<li><b>Müşteri işlem:</b> Satıcı portalındaki ürün, sipariş, abonelik ve fatura kayıtları; sözleşme onay kayıtları; form ve e-posta yazışmaları.</li>
<li><b>İşlem güvenliği:</b> Oturum bilgisi, giriş kayıtları, IP adresinin şifrelenmiş özeti.</li></ul></section>
<section id="amac"><h2>3. İşleme amaçları ve hukuki sebepler</h2><ul>
<li>Satıcı portalı hesabının açılması, siparişlerin alınması, hizmetin sunulması ve faturalandırma: bir sözleşmenin kurulması veya ifasıyla doğrudan ilgili olması (KVKK m. 5/2-c).</li>
<li>Vergi ve ticaret mevzuatından doğan saklama ve bildirim yükümlülükleri: kanunlarda açıkça öngörülmesi ve hukuki yükümlülüğün yerine getirilmesi (m. 5/2-a, ç).</li>
<li>Talep ve şikâyetlerin yanıtlanması, hizmet güvenliği, kötüye kullanım ve dolandırıcılığın önlenmesi: veri sorumlusunun meşru menfaati (m. 5/2-f).</li>
<li>Bir hakkın tesisi, kullanılması veya korunması (m. 5/2-e).</li></ul></section>
<section id="toplama"><h2>4. Toplama yöntemi</h2><p>Kişisel verileriniz; vettlo.com'daki formlar, satıcı portalı, e-posta yazışmaları ve ödeme kuruluşu aracılığıyla elektronik ortamda, otomatik yollarla toplanır.</p></section>
<section id="aktarim"><h2>5. Aktarım</h2><ul>
<li>Kişisel verileriniz yukarıdaki amaçlarla sınırlı olarak; barındırma, veri tabanı ve e-posta yönlendirme hizmeti için Cloudflare'e, e-posta gönderimi için Brevo'ya, ödemelerin alınması için ödeme kuruluşuna, ayrıca mevzuat gereği yetkili kamu kurum ve kuruluşlarına aktarılabilir.</li>
<li>Bu hizmet sağlayıcıların bir kısmının sunucuları yurt dışındadır. Yurt dışına aktarım, KVKK'nın 9. maddesinde öngörülen şartlara uygun olarak yapılır.</li></ul></section>
<section id="haklar"><h2>6. Haklarınız (KVKK m. 11)</h2><p>Veri sorumlusuna başvurarak; kişisel verilerinizin işlenip işlenmediğini öğrenme, işlenmişse bilgi talep etme, işlenme amacını ve amacına uygun kullanılıp kullanılmadığını öğrenme, yurt içinde veya yurt dışında aktarıldığı üçüncü kişileri bilme, eksik veya yanlış işlenmişse düzeltilmesini, KVKK'da öngörülen şartlar çerçevesinde silinmesini veya yok edilmesini isteme, bu işlemlerin aktarıldığı üçüncü kişilere bildirilmesini isteme, münhasıran otomatik sistemlerle analiz edilmesi sonucu aleyhinize bir sonuç çıkmasına itiraz etme ve kanuna aykırı işleme nedeniyle zarara uğramanız halinde zararın giderilmesini talep etme haklarına sahipsiniz.</p></section>
<section id="basvuru"><h2>7. Başvuru</h2><p>Başvurularınızı {_v("eposta")} adresine{(' veya ' + SELLER['kep'] + ' KEP adresine') if SELLER['kep'].strip() else ''} yazılı olarak iletebilirsiniz. Başvurular, talebin niteliğine göre en geç 30 gün içinde ücretsiz olarak sonuçlandırılır.</p></section>
""")

_INDEX_ITEMS = [("/yasal/on-bilgilendirme-formu/", "Ön Bilgilendirme Formu"), ("/yasal/mesafeli-hizmet-sozlesmesi/", "Mesafeli Hizmet Sözleşmesi"),
                ("/yasal/iptal-ve-iade/", "İptal ve İade Politikası"), ("/yasal/gizlilik/", "Gizlilik Politikası"), ("/yasal/kvkk/", "KVKK Aydınlatma Metni")]

if LEGAL_TR_READY or _PREVIEW:
    def _legal_page(path, title, desc, body):
        toc = "".join(f'<a href="{p}"{" aria-current=\"page\"" if p == path else ""}>{t}</a>' for p, t in _INDEX_ITEMS)
        page(path, f"{title} | Vettlo", desc,
             f'''<div class="wrap"><div class="page-head"><span class="eyebrow">Yasal</span><h1>{title}</h1>
<p class="small mono">Son güncelleme: {LEGAL_UPDATED}</p></div>
<div class="legal-grid"><nav class="toc" aria-label="Yasal metinler"><span class="label">Yasal metinler</span>{toc}<a href="/advertiser-terms/">Advertiser terms (EN)</a></nav>
<div class="page-body prose legal-body">{body}</div></div></div>''')
        PAGES[path]["lang"] = "tr"
        NOINDEX.add(path)

    for _p, (_t, _d, _b) in _PAGES_TR.items():
        _legal_page(_p, _t, _d, _b)
    page("/yasal/", "Yasal Metinler | Vettlo", "Vettlo'nun Türkçe yasal metinleri: ön bilgilendirme formu, mesafeli hizmet sözleşmesi, iptal ve iade politikası, gizlilik politikası ve KVKK aydınlatma metni.",
         '<div class="wrap"><div class="page-head"><span class="eyebrow">Yasal</span><h1>Yasal metinler</h1><p>Vettlo satıcı portalı üzerinden verilen siparişlere ve vettlo.com kullanımına ilişkin Türkçe yasal metinler.</p></div>'
         '<div class="page-body prose"><ul>' + "".join(f'<li><a href="{p}">{t}</a></li>' for p, t in _INDEX_ITEMS) + '</ul></div></div>')
    PAGES["/yasal/"]["lang"] = "tr"
    NOINDEX.add("/yasal/")
    FOOTER = FOOTER.replace('<a href="/terms/">Terms</a></span>', '<a href="/terms/">Terms</a> · <a href="/yasal/" lang="tr">Yasal (TR)</a></span>')
