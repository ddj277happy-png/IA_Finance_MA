window.financeKnowledge = {
  ui: {
    documentTitle: {
      en: "Annotated Dossier on Moroccan Finance",
      fr: "Dossier annoté de la finance marocaine",
      ar: "ملف مشروح حول المالية المغربية",
      zh: "摩洛哥金融注释档案"
    },
    brand: {
      en: "Morocco Finance Notes",
      fr: "Notes financières Maroc",
      ar: "ملاحظات مالية حول المغرب",
      zh: "摩洛哥金融注释"
    },
    nav: [
      { href: "#map", label: { en: "Reading Map", fr: "Carte de lecture", ar: "خريطة القراءة", zh: "阅读地图" } },
      { href: "#concepts", label: { en: "Glossary", fr: "Glossaire", ar: "مسرد", zh: "术语注释" } },
      { href: "#primers", label: { en: "Context", fr: "Repères", ar: "خلفيات", zh: "背景说明" } },
      { href: "#sources", label: { en: "Sources", fr: "Sources", ar: "المصادر", zh: "资料来源" } },
      { href: "#extend", label: { en: "Maintenance", fr: "Maintenance", ar: "الصيانة", zh: "维护扩展" } }
    ],
    hero: {
      eyebrow: {
        en: "English / French annotated mode",
        fr: "Mode annoté anglais / français",
        ar: "وضع الشرح العربي / الصيني",
        zh: "阿语 / 中文注释模式"
      },
      title: {
        en: "Annotated Dossier on Moroccan Finance",
        fr: "Dossier annoté de la finance marocaine",
        ar: "ملف مشروح حول المالية المغربية",
        zh: "摩洛哥金融注释档案"
      },
      copy: {
        en: "A bilingual annotation layer for reading sources on Moroccan banking, supervision, climate risk, participatory finance, fintech, and the French, American, and Chinese financing channels.",
        fr: "Une couche d'annotation bilingue pour lire les sources sur la banque marocaine, la supervision, les risques climatiques, la finance participative, la fintech et les canaux de financement français, américains et chinois.",
        ar: "طبقة شرح ثنائية اللغة لقراءة المصادر حول البنوك المغربية والرقابة والمخاطر المناخية والتمويل التشاركي والتكنولوجيا المالية وقنوات التمويل الفرنسية والأمريكية والصينية.",
        zh: "一个双语注释层，用来阅读摩洛哥银行业、监管、气候风险、参与式金融、金融科技，以及法国、美国、中国融资通道相关资料。"
      },
      primary: { en: "Read annotations", fr: "Lire les annotations", ar: "قراءة الشروح", zh: "阅读注释" },
      secondary: { en: "Maintain dossier", fr: "Maintenir le dossier", ar: "صيانة الملف", zh: "维护档案" }
    },
    sections: {
      map: {
        title: { en: "Reading Map", fr: "Carte de lecture", ar: "خريطة القراءة", zh: "阅读地图" },
        lead: {
          en: "These sources ask who organizes financing in Morocco, how risks enter bank balance sheets, and through which channels transnational capital produces influence.",
          fr: "Ces sources interrogent qui organise le financement au Maroc, comment les risques entrent dans les bilans bancaires et par quels canaux les capitaux transnationaux produisent leurs effets.",
          ar: "تسأل هذه المصادر من ينظم التمويل في المغرب، وكيف تدخل المخاطر إلى ميزانيات البنوك، وعبر أي قنوات يؤثر رأس المال العابر للحدود.",
          zh: "这些资料关注：摩洛哥融资由谁组织，风险如何进入银行资产负债表，跨国资本通过哪些渠道产生影响。"
        }
      },
      concepts: {
        title: { en: "Bilingual Glossary", fr: "Glossaire bilingue", ar: "مسرد ثنائي اللغة", zh: "双语术语注释" },
        lead: {
          en: "The page shows two languages at a time. The default mode is English/French; switch to Arabic/Chinese when you want a reading bridge for regional context and Chinese notes.",
          fr: "La page affiche deux langues à la fois. Le mode par défaut est anglais/français ; basculez vers arabe/chinois pour relier le contexte régional aux notes chinoises.",
          ar: "تعرض الصفحة لغتين في كل مرة. الوضع الافتراضي هو الإنجليزية/الفرنسية؛ ويمكن التبديل إلى العربية/الصينية للربط بين السياق الإقليمي والملاحظات الصينية.",
          zh: "页面一次显示两种语言。默认是英法双语；需要区域语境和中文理解时，可以切换到阿汉双语。"
        }
      },
      primers: {
        title: { en: "Context Notes", fr: "Repères contextuels", ar: "ملاحظات سياقية", zh: "背景注释" },
        lead: {
          en: "These notes put the vocabulary back into the research questions around Moroccan finance.",
          fr: "Ces repères replacent le vocabulaire dans les questions de recherche sur la finance marocaine.",
          ar: "تعيد هذه الملاحظات وضع المصطلحات داخل أسئلة البحث حول المالية المغربية.",
          zh: "这些说明把术语放回摩洛哥金融研究的问题框架中。"
        }
      },
      sources: {
        title: { en: "Reference Sources", fr: "Sources de référence", ar: "مصادر مرجعية", zh: "参考资料" },
        lead: {
          en: "The dossier annotates sources without replacing them. Data and quotations should still be checked in the originals.",
          fr: "Le dossier annote les sources sans les remplacer. Les données et citations doivent être vérifiées dans les documents originaux.",
          ar: "يشرح هذا الملف المصادر ولا يحل محلها. يجب التحقق من البيانات والاقتباسات في الوثائق الأصلية.",
          zh: "本档案用于注释资料，不替代原文。数据和引文仍需回到原始文件核对。"
        }
      },
      extend: {
        title: { en: "Dossier Maintenance", fr: "Maintenance du dossier", ar: "صيانة الملف", zh: "档案维护" },
        lead: {
          en: "The site is data-driven. Add future sources, terms, and notes mainly in data/finance-knowledge.js.",
          fr: "Le site est piloté par les données. Ajoutez les futures sources, notions et notes surtout dans data/finance-knowledge.js.",
          ar: "يعتمد الموقع على البيانات. أضف المصادر والمصطلحات والملاحظات الجديدة أساسا في data/finance-knowledge.js.",
          zh: "本页面由数据驱动。以后新增资料、术语和注释，主要修改 data/finance-knowledge.js。"
        }
      }
    },
    filters: {
      all: { en: "All", fr: "Tous", ar: "الكل", zh: "全部" },
      banking: { en: "Banking", fr: "Banque", ar: "البنوك", zh: "银行" },
      risk: { en: "Risk", fr: "Risques", ar: "المخاطر", zh: "风险" },
      capital: { en: "Capital", fr: "Capital", ar: "رأس المال", zh: "资本" },
      "new-finance": { en: "New finance", fr: "Nouveaux canaux", ar: "قنوات جديدة", zh: "新金融" }
    },
    searchPlaceholder: {
      en: "Search: nonperforming loan / risque physique / تمويل / 融资...",
      fr: "Rechercher : prêt non performant / risque physique / تمويل / 融资...",
      ar: "ابحث: قرض متعثر / risque physique / financing / 融资...",
      zh: "搜索：不良贷款 / risque physique / financing / تمويل..."
    },
    empty: {
      en: "No result. Try a shorter keyword such as risk, prêt, تمويل, or 贷款.",
      fr: "Aucun résultat. Essayez un mot-clé plus court, par exemple risk, prêt, تمويل ou 贷款.",
      ar: "لا توجد نتيجة. جرّب كلمة أقصر مثل risk أو prêt أو تمويل أو 贷款.",
      zh: "没有匹配结果。试试更短的关键词，例如 risk、prêt、تمويل 或 贷款。"
    },
    labels: {
      en: { en: "English", fr: "Anglais", ar: "الإنجليزية", zh: "英语" },
      fr: { en: "French", fr: "Français", ar: "الفرنسية", zh: "法语" },
      ar: { en: "Arabic", fr: "Arabe", ar: "العربية", zh: "阿语" },
      zh: { en: "Chinese", fr: "Chinois", ar: "الصينية", zh: "中文" }
    },
    extend: {
      stepsTitle: { en: "Update sequence", fr: "Procédure d'ajout", ar: "خطوات الإضافة", zh: "新增顺序" },
      steps: [
        {
          en: "Archive useful PDFs or annexes in references/attachments.",
          fr: "Archivez les PDF ou annexes utiles dans references/attachments.",
          ar: "ضع ملفات PDF أو الملاحق المفيدة في references/attachments.",
          zh: "把有用的 PDF 或附件放进 references/attachments。"
        },
        {
          en: "Add the source metadata and reading purpose under sources.",
          fr: "Ajoutez les métadonnées et l'usage de lecture dans sources.",
          ar: "أضف بيانات المصدر وغرض القراءة في sources.",
          zh: "在 sources 中加入资料元数据和阅读用途。"
        },
        {
          en: "Add difficult concepts under concepts with four language fields.",
          fr: "Ajoutez les notions difficiles dans concepts avec quatre champs linguistiques.",
          ar: "أضف المفاهيم الصعبة في concepts مع الحقول اللغوية الأربعة.",
          zh: "把难理解的概念加入 concepts，并补齐四语字段。"
        },
        {
          en: "If the research frame changes, add a card to primers or mapCards.",
          fr: "Si le cadre de recherche change, ajoutez une carte dans primers ou mapCards.",
          ar: "إذا تغير إطار البحث، أضف بطاقة في primers أو mapCards.",
          zh: "如果研究框架变化，就在 primers 或 mapCards 中新增卡片。"
        }
      ],
      templateTitle: { en: "Concept template", fr: "Modèle d'entrée", ar: "قالب المصطلح", zh: "术语模板" }
    },
    footer: {
      en: "Annotated dossier for the IA_Finance_MA reference library. Data lives in data/finance-knowledge.js; hero image lives in assets/finance-learning-hero.png.",
      fr: "Dossier annoté pour la bibliothèque IA_Finance_MA. Les données sont dans data/finance-knowledge.js ; l'image d'en-tête est dans assets/finance-learning-hero.png.",
      ar: "ملف مشروح لمكتبة IA_Finance_MA. توجد البيانات في data/finance-knowledge.js، وتوجد صورة الواجهة في assets/finance-learning-hero.png.",
      zh: "IA_Finance_MA 参考资料库的注释档案。数据位于 data/finance-knowledge.js；横幅图位于 assets/finance-learning-hero.png。"
    }
  },

  mapCards: [
    {
      tag: { en: "Banking", fr: "Banque", ar: "البنوك", zh: "银行" },
      tone: "teal",
      title: {
        en: "Banks are the operating base",
        fr: "Le secteur bancaire constitue le socle",
        ar: "البنوك هي القاعدة التشغيلية",
        zh: "银行体系是底盘"
      },
      body: {
        en: "Morocco's financial system is largely bank-led. Loans, deposits, solvency, and bad loans are the basic grammar for reading risks and capital flows.",
        fr: "Le système financier marocain est largement dominé par les banques. Prêts, dépôts, solvabilité et créances en souffrance forment la grammaire de base des risques et flux de capitaux.",
        ar: "يقود القطاع البنكي جزءا كبيرا من النظام المالي المغربي. لذلك تشكل القروض والودائع والملاءة والقروض المتعثرة لغة أساسية لفهم المخاطر وتدفقات رأس المال.",
        zh: "摩洛哥金融体系很大程度上由银行主导。贷款、存款、偿付能力和不良贷款，是理解风险和资本流动的基础语法。"
      }
    },
    {
      tag: { en: "Climate", fr: "Climat", ar: "المناخ", zh: "气候" },
      tone: "red",
      title: {
        en: "Climate risk becomes financial risk",
        fr: "Le risque climatique devient un risque financier",
        ar: "الخطر المناخي يتحول إلى خطر مالي",
        zh: "气候风险会变成金融风险"
      },
      body: {
        en: "Droughts, floods, and the low-carbon transition affect repayment capacity, loan portfolios, and prudential stress tests.",
        fr: "Sécheresses, inondations et transition bas carbone affectent la capacité de remboursement, les portefeuilles de prêts et les tests de résistance prudentiels.",
        ar: "تؤثر الجفافات والفيضانات والانتقال منخفض الكربون في قدرة السداد ومحافظ القروض واختبارات الضغط الرقابية.",
        zh: "干旱、洪水和低碳转型会影响借款人还款能力、银行贷款组合和监管压力测试。"
      }
    },
    {
      tag: { en: "Capital", fr: "Capital", ar: "رأس المال", zh: "资本" },
      tone: "gold",
      title: {
        en: "External influence takes different financial forms",
        fr: "Les influences extérieures prennent des formes financières distinctes",
        ar: "التأثير الخارجي له أشكال مالية مختلفة",
        zh: "外部影响有不同金融形态"
      },
      body: {
        en: "France appears through banking history and regulatory legacies; the United States through development finance; China through infrastructure, energy, minerals, and value chains.",
        fr: "La France renvoie à l'histoire bancaire et aux héritages réglementaires ; les États-Unis à la finance de développement ; la Chine aux infrastructures, à l'énergie, aux minerais et aux chaînes de valeur.",
        ar: "يظهر أثر فرنسا عبر التاريخ البنكي والإرث التنظيمي، والولايات المتحدة عبر تمويل التنمية، والصين عبر البنية التحتية والطاقة والمعادن وسلاسل القيمة.",
        zh: "法国更多体现为银行历史和监管遗产，美国更多体现为发展金融，中国资本则常与基础设施、能源、矿产和价值链相连。"
      }
    },
    {
      tag: { en: "New Finance", fr: "Nouveaux canaux", ar: "قنوات جديدة", zh: "新金融" },
      tone: "blue",
      title: {
        en: "New finance shifts the access point",
        fr: "Les nouveaux canaux déplacent le point d'accès",
        ar: "القنوات المالية الجديدة تغير نقطة الوصول",
        zh: "新金融改变金融入口"
      },
      body: {
        en: "Participatory finance, embedded finance, open banking, and platform credit all ask who delivers credit to firms and households.",
        fr: "Finance participative, finance embarquée, open banking et crédit de plateforme posent la même question : qui distribue le crédit aux entreprises et aux ménages ?",
        ar: "التمويل التشاركي والتمويل المدمج والخدمات المصرفية المفتوحة وائتمان المنصات تطرح سؤالا واحدا: من يوزع الائتمان على الشركات والأسر؟",
        zh: "参与式金融、嵌入式金融、开放银行和平台信贷，都在追问：谁把信用送到企业和家庭手中？"
      }
    }
  ],

  primers: [
    {
      title: {
        en: "1. Why start with banks?",
        fr: "1. Pourquoi commencer par les banques ?",
        ar: "1. لماذا نبدأ بالبنوك؟",
        zh: "1. 为什么总是从银行讲起？"
      },
      body: {
        en: "The World Bank/BAM report focuses on banks because credit institutions dominate financial-sector assets. Morocco has 19 banks, including domestic private banks, public banks, and majority foreign-owned banks. This means that financing is often first read as bank credit.",
        fr: "Le rapport World Bank/BAM place les banques au centre parce que les établissements de crédit dominent les actifs du secteur financier. Le Maroc compte 19 banques, entre banques privées domestiques, banques publiques et banques majoritairement étrangères. Le financement se lit donc souvent d'abord comme crédit bancaire.",
        ar: "يركز تقرير البنك الدولي وبنك المغرب على البنوك لأن مؤسسات الائتمان تهيمن على أصول القطاع المالي. ويضم المغرب 19 بنكا، بين بنوك خاصة محلية وبنوك عمومية وبنوك ذات ملكية أجنبية أغلبية. لذلك يقرأ التمويل غالبا أولا كائتمان بنكي.",
        zh: "世界银行/摩洛哥央行报告把银行置于中心，是因为信用机构在金融部门资产中占主导。摩洛哥有 19 家银行，包括本土私人银行、国有银行和外资控股银行。因此，“融资渠道”很多时候首先是银行信贷渠道。"
      }
    },
    {
      title: {
        en: "2. The balance sheet is the grammar of risk reports",
        fr: "2. Le bilan est la grammaire des rapports de risque",
        ar: "2. الميزانية هي نحو تقارير المخاطر",
        zh: "2. 资产负债表是风险报告的核心语法"
      },
      body: {
        en: "A bank's assets are mainly loans and securities; its liabilities are mainly deposits and funding. Capital is the cushion. Climate shocks, industrial transition, and foreign capital shifts ultimately show up in loan quality, solvency, profit, and liquidity.",
        fr: "Les actifs d'une banque sont surtout prêts et titres ; ses passifs sont surtout dépôts et financements. Le capital sert de coussin. Chocs climatiques, transition industrielle et variations de capitaux extérieurs se lisent dans la qualité des prêts, la solvabilité, les profits et la liquidité.",
        ar: "تتكون أصول البنك أساسا من القروض والأوراق المالية، أما خصومه فمن الودائع والتمويل. رأس المال هو الوسادة الواقية. وتظهر الصدمات المناخية والتحول الصناعي وتغيرات رأس المال الأجنبي في جودة القروض والملاءة والأرباح والسيولة.",
        zh: "银行资产端主要是贷款和证券，负债端主要是存款和融资，资本是缓冲垫。气候冲击、产业转型或外部资本变化，最终都会反映在贷款质量、偿付能力、利润和流动性上。"
      }
    },
    {
      title: {
        en: "3. France, the United States, and China do not act through the same channel",
        fr: "3. France, États-Unis et Chine n'agissent pas par le même canal",
        ar: "3. فرنسا والولايات المتحدة والصين لا تعمل عبر القناة نفسها",
        zh: "3. 法国、美国、中国不是同一种影响"
      },
      body: {
        en: "The French track often concerns historical banking networks and retail-bank recomposition. The American track is closer to development finance and investment facilitation. The Chinese track has moved from infrastructure toward new energy, critical minerals, and automotive chains.",
        fr: "La piste française concerne souvent les réseaux bancaires historiques et la recomposition de la banque de détail. La piste américaine relève plutôt de la finance de développement et de la facilitation de l'investissement. La piste chinoise va des infrastructures vers les énergies nouvelles, les minerais critiques et les chaînes automobiles.",
        ar: "يرتبط المسار الفرنسي غالبا بالشبكات البنكية التاريخية وإعادة تشكيل بنوك التجزئة. أما المسار الأمريكي فأقرب إلى تمويل التنمية وتسهيل الاستثمار. ويتحرك المسار الصيني من البنية التحتية نحو الطاقة الجديدة والمعادن الحرجة وسلاسل السيارات.",
        zh: "法国线索常涉及历史银行网络和零售银行重组；美国线索更偏发展金融和投资便利化；中国线索则从基础设施转向新能源、关键矿产和汽车产业链。"
      }
    },
    {
      title: {
        en: "4. Islamic finance is often called participatory finance in Morocco",
        fr: "4. La finance islamique est souvent appelée finance participative",
        ar: "4. تسمى المالية الإسلامية في المغرب غالبا تمويلا تشاركيا",
        zh: "4. 伊斯兰金融在摩洛哥常称为参与式金融"
      },
      body: {
        en: "Participatory finance does not simply replace the banking system. It works as a regulated product line inside the system. The key question is whether it expands financial inclusion, serves SMEs, or is absorbed by large banking groups.",
        fr: "La finance participative ne remplace pas simplement le système bancaire. Elle fonctionne comme une ligne de produits réglementée dans le système. La question est de savoir si elle élargit l'inclusion financière, sert les PME ou reste absorbée par les grands groupes bancaires.",
        ar: "لا يحل التمويل التشاركي ببساطة محل النظام البنكي، بل يعمل كخط منتجات منظم داخله. والسؤال هو هل يوسع الشمول المالي ويخدم المقاولات الصغرى والمتوسطة أم يبقى مستوعبا داخل المجموعات البنكية الكبرى.",
        zh: "参与式金融并不是简单替代银行体系，更像是在监管框架下进入传统体系的产品线。关键是看它是否扩大金融包容性、服务中小企业，还是被大型银行集团吸收。"
      }
    },
    {
      title: {
        en: "5. Climate reports study transmission into banks",
        fr: "5. Les rapports climatiques analysent la transmission vers les banques",
        ar: "5. تقارير المناخ تدرس انتقال الأثر إلى البنوك",
        zh: "5. 气候风险报告关注冲击如何传导到银行"
      },
      body: {
        en: "Droughts affect agriculture, food processing, tourism, and water-intensive sectors. Floods damage assets and infrastructure. Low-carbon transition affects high-emission sectors or sectors exposed to the EU CBAM. Bank risk depends on sectoral and regional loan exposure.",
        fr: "Les sécheresses touchent l'agriculture, l'agroalimentaire, le tourisme et les secteurs intensifs en eau. Les inondations endommagent actifs et infrastructures. La transition bas carbone affecte les secteurs émetteurs ou exposés au CBAM européen. Le risque bancaire dépend des expositions sectorielles et régionales.",
        ar: "يؤثر الجفاف في الفلاحة والصناعات الغذائية والسياحة والقطاعات كثيفة استعمال الماء. وتضر الفيضانات بالأصول والبنية التحتية. كما يؤثر الانتقال منخفض الكربون في القطاعات عالية الانبعاث أو المعرضة لآلية الكربون الأوروبية. لذلك يعتمد الخطر البنكي على التعرض القطاعي والمجالي.",
        zh: "干旱影响农业、食品加工、旅游和用水密集行业；洪水损坏资产和基础设施；低碳转型影响高排放或受欧盟 CBAM 影响的行业。银行风险来自贷款组合的行业和地区暴露。"
      }
    },
    {
      title: {
        en: "6. Fintech changes access and distribution",
        fr: "6. La fintech change l'accès et la distribution",
        ar: "6. التكنولوجيا المالية تغير الوصول والتوزيع",
        zh: "6. 金融科技改变入口和分发方式"
      },
      body: {
        en: "Embedded finance, open banking, and BaaS are not just better apps. They mean that payment, credit, and insurance can be placed inside e-commerce, logistics, and enterprise software workflows.",
        fr: "Finance embarquée, open banking et BaaS ne sont pas seulement de meilleures applications. Ils signifient que paiement, crédit et assurance peuvent être intégrés à l'e-commerce, à la logistique et aux logiciels d'entreprise.",
        ar: "التمويل المدمج والخدمات المصرفية المفتوحة والبنوك كخدمة ليست مجرد تطبيقات أفضل، بل تعني إدماج الدفع والائتمان والتأمين داخل التجارة الإلكترونية واللوجستيك وبرمجيات الشركات.",
        zh: "嵌入式金融、开放银行和 BaaS 不只是更好的 App，而是支付、信贷、保险可以被放进电商、物流和企业软件流程中。"
      }
    }
  ],

  flowSteps: [
    {
      title: { en: "Real-world shock", fr: "Choc réel", ar: "صدمة واقعية", zh: "现实冲击" },
      body: { en: "Drought, flood, energy prices, industrial policy, or foreign-investment shifts.", fr: "Sécheresse, inondation, prix de l'énergie, politique industrielle ou variation des investissements étrangers.", ar: "جفاف أو فيضان أو أسعار الطاقة أو السياسة الصناعية أو تغير الاستثمار الأجنبي.", zh: "干旱、洪水、能源价格、产业政策或外国投资变化。" }
    },
    {
      title: { en: "Firms and households", fr: "Entreprises et ménages", ar: "الشركات والأسر", zh: "企业与家庭" },
      body: { en: "Lower income, higher costs, damaged assets, and weaker repayment capacity.", fr: "Revenus plus faibles, coûts plus élevés, actifs endommagés et capacité de remboursement réduite.", ar: "دخل أقل وتكاليف أعلى وأصول متضررة وقدرة سداد أضعف.", zh: "收入下降、成本上升、资产受损，还款能力变弱。" }
    },
    {
      title: { en: "Bank assets", fr: "Actifs bancaires", ar: "أصول البنوك", zh: "银行资产" },
      body: { en: "Higher default probabilities, more nonperforming loans, pressure on profits and capital.", fr: "Hausse des probabilités de défaut, davantage de prêts non performants, pression sur les profits et le capital.", ar: "ارتفاع احتمال التعثر وزيادة القروض المتعثرة وضغط على الأرباح ورأس المال.", zh: "违约概率上升，不良贷款增加，利润和资本承压。" }
    },
    {
      title: { en: "Prudential response", fr: "Réponse prudentielle", ar: "استجابة احترازية", zh: "监管反应" },
      body: { en: "Stress tests, capital requirements, disclosure, green taxonomy, and risk governance.", fr: "Tests de résistance, exigences de capital, divulgation, taxonomie verte et gouvernance des risques.", ar: "اختبارات ضغط ومتطلبات رأس المال والإفصاح والتصنيف الأخضر وحوكمة المخاطر.", zh: "压力测试、资本要求、信息披露、绿色分类法和风险治理。" }
    }
  ],

  sources: [
    {
      meta: ["2024", "World Bank / BAM", "PDF"],
      title: "Assessing Climate Physical and Transition Risks for the Moroccan Banking Sector",
      body: {
        en: "Core source on banking structure, physical climate risk, transition risk, stress testing, and prudential response.",
        fr: "Source centrale sur la structure bancaire, les risques climatiques physiques, les risques de transition, les tests de résistance et la réponse prudentielle.",
        ar: "مصدر أساسي حول بنية القطاع البنكي والمخاطر المناخية المادية ومخاطر الانتقال واختبارات الضغط والاستجابة الرقابية.",
        zh: "关于银行结构、气候物理风险、转型风险、压力测试和监管响应的核心资料。"
      },
      url: "references/attachments/world-bank-bank-al-maghrib-climate-risks-moroccan-banking-sector-2024.pdf",
      linkLabel: { en: "Open local PDF", fr: "Ouvrir le PDF local", ar: "فتح PDF المحلي", zh: "打开本地 PDF" }
    },
    {
      meta: ["2024", "OECD", "Country survey"],
      title: "OECD Economic Surveys: Morocco 2024",
      body: {
        en: "Macro and policy background for financial regulation, capital flows, foreign banks, and financial inclusion.",
        fr: "Cadre macroéconomique et politique pour la réglementation financière, les flux de capitaux, les banques étrangères et l'inclusion financière.",
        ar: "خلفية اقتصادية وسياساتية حول التنظيم المالي وتدفقات رأس المال والبنوك الأجنبية والشمول المالي.",
        zh: "关于金融监管、资本流动、外资银行和金融包容性的宏观经济与政策背景。"
      },
      url: "https://www.oecd-ilibrary.org/en/publications/oecd-economic-surveys-morocco-2024_80777ea7-en.html",
      linkLabel: { en: "Open page", fr: "Ouvrir la page", ar: "فتح الصفحة", zh: "打开网页" }
    },
    {
      meta: ["2026", "McKinsey", "Banking"],
      title: "From potential to performance: A snapshot of African banking",
      body: {
        en: "Consulting-style benchmark for African banking scale, profitability, digitization, and country comparisons.",
        fr: "Repère de conseil sur la taille, la rentabilité, la numérisation et les comparaisons nationales de la banque africaine.",
        ar: "مرجع بأسلوب استشاري حول حجم البنوك الإفريقية وربحيتها ورقمنتها والمقارنات بين الدول.",
        zh: "关于非洲银行业规模、盈利能力、数字化和国家比较的咨询式参考。"
      },
      url: "https://www.mckinsey.com/industries/financial-services/our-insights/from-potential-to-performance-a-snapshot-of-african-banking",
      linkLabel: { en: "Open page", fr: "Ouvrir la page", ar: "فتح الصفحة", zh: "打开网页" }
    },
    {
      meta: ["2026", "Deloitte", "Fintech"],
      title: "Finance embarquée au Maroc",
      body: {
        en: "Context on embedded finance, open banking, BaaS, platform finance, and new credit-distribution channels.",
        fr: "Contexte sur la finance embarquée, l'open banking, le BaaS, la finance de plateforme et les nouveaux canaux de distribution du crédit.",
        ar: "خلفية حول التمويل المدمج والخدمات المصرفية المفتوحة والبنوك كخدمة وتمويل المنصات وقنوات توزيع الائتمان الجديدة.",
        zh: "关于嵌入式金融、开放银行、BaaS、平台金融和新信贷分发渠道的背景。"
      },
      url: "https://www.deloitte.com/afrique/fr/Industries/financial-services/perspectives/finance-embarquee-au-maroc.html",
      linkLabel: { en: "Open page", fr: "Ouvrir la page", ar: "فتح الصفحة", zh: "打开网页" }
    },
    {
      meta: ["2020", "DFC", "Development finance"],
      title: "DFC initiatives to expand U.S. investment in Morocco",
      body: {
        en: "Entry point on U.S. development finance, Prosper Africa, and Morocco as a regional investment platform.",
        fr: "Point d'entrée sur la finance de développement américaine, Prosper Africa et le Maroc comme plateforme régionale d'investissement.",
        ar: "مدخل إلى تمويل التنمية الأمريكي ومبادرة Prosper Africa والمغرب كمنصة استثمار إقليمية.",
        zh: "关于美国发展金融、Prosper Africa，以及摩洛哥作为区域投资平台的入口资料。"
      },
      url: "https://www.dfc.gov/media/press-releases/dfc-announces-initiatives-expand-us-investment-and-development-morocco",
      linkLabel: { en: "Open page", fr: "Ouvrir la page", ar: "فتح الصفحة", zh: "打开网页" }
    },
    {
      meta: ["2025", "Congiu", "China capital"],
      title: "Mapping Chinese capital in Morocco (2004-2024)",
      body: {
        en: "Research track on the shift of Chinese capital from infrastructure toward new energy, critical minerals, and automotive chains.",
        fr: "Piste de recherche sur le déplacement des capitaux chinois des infrastructures vers les énergies nouvelles, les minerais critiques et les chaînes automobiles.",
        ar: "مسار بحثي حول انتقال رأس المال الصيني من البنية التحتية إلى الطاقة الجديدة والمعادن الحرجة وسلاسل السيارات.",
        zh: "关于中国资本从基础设施转向新能源、关键矿产和汽车产业链的研究线索。"
      },
      url: "https://www.rivisteweb.it/doi/10.82002/119545",
      linkLabel: { en: "Open page", fr: "Ouvrir la page", ar: "فتح الصفحة", zh: "打开网页" }
    }
  ],

  concepts: [
    { id: "Banking sector", category: "banking", terms: { en: "Banking sector", fr: "Secteur bancaire", ar: "القطاع البنكي", zh: "银行业" }, notes: { en: { plain: "The set of banks and credit institutions that collect deposits, make loans, process payments, and create credit.", use: "The base layer for understanding access to finance in Morocco." }, fr: { plain: "Ensemble des banques et institutions de crédit qui collectent les dépôts, accordent des prêts, assurent les paiements et créent du crédit.", use: "Le socle pour comprendre l'accès au financement au Maroc." }, ar: { plain: "مجموعة البنوك ومؤسسات الائتمان التي تجمع الودائع وتمنح القروض وتدير المدفوعات وتخلق الائتمان.", use: "قاعدة لفهم الوصول إلى التمويل في المغرب." }, zh: { plain: "吸收存款、发放贷款、处理支付并创造信用的银行和信用机构体系。", use: "理解摩洛哥融资可得性的底层概念。" } } },
    { id: "Balance sheet", category: "banking", terms: { en: "Balance sheet", fr: "Bilan", ar: "الميزانية العمومية", zh: "资产负债表" }, notes: { en: { plain: "A table showing what a bank owns, what it owes, and the capital cushion that remains.", use: "Loan deterioration or capital pressure ultimately appears in the balance sheet." }, fr: { plain: "Tableau qui montre les actifs d'une banque, ses passifs et le capital qui reste comme coussin de sécurité.", use: "La dégradation des prêts ou la pression sur le capital se lit dans le bilan." }, ar: { plain: "جدول يوضح ما يملكه البنك وما عليه من التزامات ورأس المال المتبقي كوسادة أمان.", use: "تدهور القروض أو الضغط على رأس المال يظهر في الميزانية." }, zh: { plain: "展示银行拥有什么资产、欠什么负债、剩多少资本缓冲的表。", use: "贷款恶化或资本压力最终会反映在资产负债表上。" } } },
    { id: "Loan portfolio", category: "banking", terms: { en: "Loan portfolio", fr: "Portefeuille de prêts", ar: "محفظة القروض", zh: "贷款组合" }, notes: { en: { plain: "The full set of loans made by a bank, distributed by sector, region, borrower type, and maturity.", use: "Used to see whether a bank is exposed to agriculture, industry, tourism, or flood-prone regions." }, fr: { plain: "Ensemble des prêts accordés par une banque, répartis par secteur, région, type de client et maturité.", use: "Sert à mesurer l'exposition à l'agriculture, à l'industrie, au tourisme ou aux zones inondables." }, ar: { plain: "مجموعة القروض التي يمنحها البنك حسب القطاع والمنطقة ونوع العميل والأجل.", use: "تستخدم لقياس التعرض للفلاحة أو الصناعة أو السياحة أو مناطق الفيضانات." }, zh: { plain: "银行发放的一整组贷款，按行业、地区、客户类型和期限分布。", use: "用于判断银行是否暴露于农业、工业、旅游或洪水高风险地区。" } } },
    { id: "Deposit", category: "banking", terms: { en: "Deposit", fr: "Dépôt", ar: "وديعة", zh: "存款" }, notes: { en: { plain: "Money placed by customers at a bank; for the bank it is a funding source and a liability.", use: "Deposit stability affects the bank's capacity to lend and financial stability." }, fr: { plain: "Argent placé par les clients auprès d'une banque ; pour la banque, c'est une ressource et un passif.", use: "La stabilité des dépôts influence la capacité de prêt et la stabilité financière." }, ar: { plain: "أموال يضعها العملاء لدى البنك؛ وهي مصدر تمويل للبنك والتزام عليه.", use: "استقرار الودائع يؤثر في قدرة البنك على الإقراض وفي الاستقرار المالي." }, zh: { plain: "客户放在银行的钱；对银行而言是资金来源，也是一项负债。", use: "存款稳定性影响银行放贷能力和金融稳定。" } } },
    { id: "Nonperforming loan", category: "risk", terms: { en: "Nonperforming loan (NPL)", fr: "Prêt non performant", ar: "قرض متعثر", zh: "不良贷款" }, notes: { en: { plain: "A loan on which the borrower no longer pays principal or interest normally.", use: "Climate or economic shocks can raise NPLs by weakening repayment capacity." }, fr: { plain: "Prêt pour lequel l'emprunteur ne rembourse plus normalement le principal ou les intérêts.", use: "Les chocs climatiques ou économiques peuvent augmenter les NPL en affaiblissant la capacité de remboursement." }, ar: { plain: "قرض لم يعد المقترض يسدد أصله أو فوائده بشكل طبيعي.", use: "الصدمات المناخية أو الاقتصادية قد ترفع القروض المتعثرة عبر إضعاف القدرة على السداد." }, zh: { plain: "借款人已不能正常偿还本金或利息的贷款。", use: "气候或经济冲击会削弱还款能力，从而推高不良贷款。" } } },
    { id: "Capital adequacy ratio", category: "risk", terms: { en: "Capital adequacy ratio (CAR)", fr: "Ratio de solvabilité", ar: "نسبة كفاية رأس المال", zh: "资本充足率" }, notes: { en: { plain: "The ratio of bank capital to risk-weighted assets; it measures loss-absorbing capacity.", use: "Stress tests check whether CAR remains sufficient after shocks." }, fr: { plain: "Rapport entre le capital d'une banque et ses actifs pondérés par les risques ; il mesure sa capacité à absorber des pertes.", use: "Les tests de résistance vérifient si ce ratio reste suffisant après des chocs." }, ar: { plain: "نسبة رأس مال البنك إلى الأصول المرجحة بالمخاطر؛ تقيس القدرة على امتصاص الخسائر.", use: "تتحقق اختبارات الضغط مما إذا بقيت النسبة كافية بعد الصدمات." }, zh: { plain: "银行资本相对于风险加权资产的比例，衡量吸收损失的能力。", use: "压力测试会检查冲击后资本充足率是否仍然足够。" } } },
    { id: "Risk-weighted assets", category: "risk", terms: { en: "Risk-weighted assets (RWA)", fr: "Actifs pondérés par les risques", ar: "الأصول المرجحة بالمخاطر", zh: "风险加权资产" }, notes: { en: { plain: "Assets adjusted by their risk level and used to calculate regulatory capital needs.", use: "Two loans of the same size may require different capital if their risks differ." }, fr: { plain: "Actifs ajustés selon leur niveau de risque et utilisés pour calculer le capital réglementaire nécessaire.", use: "Deux prêts de même montant peuvent exiger des niveaux de capital différents." }, ar: { plain: "أصول تعدل بحسب مستوى المخاطر وتستخدم لحساب رأس المال التنظيمي المطلوب.", use: "قد يتطلب قرضان بالمبلغ نفسه رأسمالا مختلفا إذا اختلفت مخاطرهما." }, zh: { plain: "按风险程度加权后的资产总额，用于计算监管资本需求。", use: "同样金额的贷款，如果风险不同，资本要求也可能不同。" } } },
    { id: "Probability of default", category: "risk", terms: { en: "Probability of default (PD)", fr: "Probabilité de défaut", ar: "احتمال التعثر", zh: "违约概率" }, notes: { en: { plain: "The probability that a borrower will fail to repay over a given period.", use: "Climate shocks can increase PD through lower income, higher costs, or asset losses." }, fr: { plain: "Probabilité qu'un emprunteur ne rembourse pas sur une période donnée.", use: "Un choc climatique peut augmenter la PD via baisse de revenus, hausse des coûts ou pertes d'actifs." }, ar: { plain: "احتمال أن يفشل المقترض في السداد خلال فترة معينة.", use: "قد ترفع الصدمات المناخية هذا الاحتمال عبر انخفاض الدخل أو ارتفاع التكاليف أو خسارة الأصول." }, zh: { plain: "借款人在某一时期内无法偿还债务的可能性。", use: "气候冲击会通过收入下降、成本上升或资产损失提高违约概率。" } } },
    { id: "Exposure", category: "risk", terms: { en: "Exposure", fr: "Exposition", ar: "التعرض للمخاطر", zh: "风险暴露" }, notes: { en: { plain: "The amount a bank has committed to a sector, region, client, or risk source.", use: "Reports ask how exposed banks are to agriculture, flood zones, or transition-sensitive sectors." }, fr: { plain: "Montant engagé par une banque envers un secteur, une région, un client ou une source de risque.", use: "Les rapports demandent l'exposition des banques à l'agriculture, aux zones inondables ou aux secteurs sensibles à la transition." }, ar: { plain: "المبلغ الذي يلتزم به البنك تجاه قطاع أو منطقة أو عميل أو مصدر خطر.", use: "تسأل التقارير عن تعرض البنوك للفلاحة أو مناطق الفيضانات أو القطاعات الحساسة للانتقال." }, zh: { plain: "银行对某一行业、地区、客户或风险源投入的资金规模。", use: "报告常问银行对农业、洪水地区或转型敏感行业的暴露有多大。" } } },
    { id: "Concentration risk", category: "risk", terms: { en: "Concentration risk", fr: "Risque de concentration", ar: "مخاطر التركز", zh: "集中度风险" }, notes: { en: { plain: "Risk created when assets or loans are too concentrated in a few banks, sectors, clients, or regions.", use: "Important because Morocco's largest banks hold a high share of banking assets." }, fr: { plain: "Risque créé par une concentration excessive des actifs ou prêts dans quelques banques, secteurs, clients ou régions.", use: "Notion importante car les plus grandes banques marocaines concentrent une part élevée des actifs." }, ar: { plain: "خطر ينشأ عندما تتركز الأصول أو القروض في عدد محدود من البنوك أو القطاعات أو العملاء أو المناطق.", use: "مهم لأن أكبر البنوك المغربية تستحوذ على حصة كبيرة من الأصول البنكية." }, zh: { plain: "资产或贷款过度集中在少数银行、行业、客户或地区时产生的风险。", use: "摩洛哥大型银行资产占比较高，因此集中度风险很关键。" } } },
    { id: "Physical climate risk", category: "risk", terms: { en: "Physical climate risk", fr: "Risque climatique physique", ar: "المخاطر المناخية المادية", zh: "气候物理风险" }, notes: { en: { plain: "Financial risk from climate events such as droughts, floods, sea-level rise, or heat waves.", use: "For Morocco, drought, water stress, and floods are especially important." }, fr: { plain: "Risque financier provenant d'événements climatiques comme sécheresse, inondation, montée du niveau de la mer ou vague de chaleur.", use: "Au Maroc, sécheresse, stress hydrique et inondations sont particulièrement importants." }, ar: { plain: "خطر مالي ناتج عن أحداث مناخية مثل الجفاف والفيضانات وارتفاع مستوى البحر وموجات الحرارة.", use: "في المغرب، الجفاف والإجهاد المائي والفيضانات ذات أهمية خاصة." }, zh: { plain: "由干旱、洪水、海平面上升或热浪等气候事件引发的金融风险。", use: "在摩洛哥，干旱、水资源压力和洪水尤其重要。" } } },
    { id: "Transition risk", category: "risk", terms: { en: "Transition risk", fr: "Risque de transition", ar: "مخاطر الانتقال", zh: "转型风险" }, notes: { en: { plain: "Financial risk from policy, technology, market, or trade changes linked to the low-carbon transition.", use: "Electricity, transport, mining, manufacturing, agriculture, and CBAM-exposed sectors can be sensitive." }, fr: { plain: "Risque financier lié aux changements de politiques, technologies, marchés ou règles commerciales de la transition bas carbone.", use: "Électricité, transport, mines, industrie, agriculture et secteurs exposés au CBAM peuvent être sensibles." }, ar: { plain: "خطر مالي ناتج عن تغيرات السياسات أو التكنولوجيا أو الأسواق أو قواعد التجارة المرتبطة بالانتقال منخفض الكربون.", use: "قد تكون الكهرباء والنقل والمناجم والصناعة والفلاحة والقطاعات المعرضة لـ CBAM حساسة." }, zh: { plain: "由低碳转型相关政策、技术、市场或贸易规则变化带来的金融风险。", use: "电力、运输、采矿、制造业、农业及受 CBAM 影响行业可能较敏感。" } } },
    { id: "Stress test", category: "risk", terms: { en: "Stress test", fr: "Test de résistance", ar: "اختبار الضغط", zh: "压力测试" }, notes: { en: { plain: "An exercise applying an extreme but plausible scenario to assess resilience.", use: "Climate scenarios estimate effects on NPL, PD, and CAR." }, fr: { plain: "Exercice appliquant un scénario extrême mais plausible pour évaluer la résistance.", use: "Les scénarios climatiques estiment les effets sur NPL, PD et CAR." }, ar: { plain: "تمرين يطبق سيناريو حادا لكنه ممكن لتقييم القدرة على الصمود.", use: "تقدر سيناريوهات المناخ الأثر على القروض المتعثرة واحتمال التعثر وكفاية رأس المال." }, zh: { plain: "用极端但可能发生的情景检验银行或体系韧性的练习。", use: "气候情景用于估算对不良贷款、违约概率和资本充足率的影响。" } } },
    { id: "Transmission channel", category: "risk", terms: { en: "Transmission channel", fr: "Canal de transmission", ar: "قناة انتقال الأثر", zh: "传导渠道" }, notes: { en: { plain: "The path through which a real-world shock enters the economy and financial system.", use: "A drought can reduce farm output, then firm income, then loan quality." }, fr: { plain: "Chemin par lequel un choc réel entre dans l'économie puis dans le système financier.", use: "Une sécheresse peut réduire la production agricole, puis les revenus des entreprises, puis la qualité des prêts." }, ar: { plain: "المسار الذي تنتقل عبره الصدمة الواقعية إلى الاقتصاد ثم إلى النظام المالي.", use: "قد يخفض الجفاف الإنتاج الفلاحي ثم دخل الشركات ثم جودة القروض." }, zh: { plain: "现实冲击进入经济和金融系统的路径。", use: "干旱可能先降低农业产量，再影响企业收入，最后影响贷款质量。" } } },
    { id: "Prudential supervision", category: "risk", terms: { en: "Prudential supervision", fr: "Supervision prudentielle", ar: "الرقابة الاحترازية", zh: "审慎监管" }, notes: { en: { plain: "Regulatory oversight designed to preserve bank soundness and financial stability.", use: "Bank Al-Maghrib is central for climate-risk guidance, stress testing, and disclosure." }, fr: { plain: "Surveillance réglementaire visant à préserver la solidité des banques et la stabilité financière.", use: "Bank Al-Maghrib est central pour les risques climatiques, les tests de résistance et la divulgation." }, ar: { plain: "رقابة تنظيمية تهدف إلى الحفاظ على متانة البنوك والاستقرار المالي.", use: "يلعب بنك المغرب دورا مركزيا في توجيه مخاطر المناخ واختبارات الضغط والإفصاح." }, zh: { plain: "监管机构为维护银行稳健和金融稳定而进行的监督。", use: "摩洛哥央行在气候风险指引、压力测试和披露方面扮演核心角色。" } } },
    { id: "Green taxonomy", category: "risk", terms: { en: "Green taxonomy", fr: "Taxonomie verte", ar: "التصنيف الأخضر", zh: "绿色分类法" }, notes: { en: { plain: "A classification system defining which activities count as green or sustainable.", use: "It limits greenwashing in finance and reporting." }, fr: { plain: "Système de classification définissant quelles activités sont vertes ou durables.", use: "Elle limite le greenwashing dans le financement et le reporting." }, ar: { plain: "نظام تصنيف يحدد الأنشطة التي تعد خضراء أو مستدامة.", use: "يحد من غسل السمعة الخضراء في التمويل والتقارير." }, zh: { plain: "界定哪些经济活动可被视为绿色或可持续的分类体系。", use: "用于减少金融和披露中的“漂绿”。" } } },
    { id: "Climate disclosure", category: "risk", terms: { en: "Climate disclosure", fr: "Publication d'informations climatiques", ar: "الإفصاح المناخي", zh: "气候信息披露" }, notes: { en: { plain: "Publication of climate risks, emissions, and management practices by firms or banks.", use: "Without disclosure, banks struggle to assess client transition and physical risks." }, fr: { plain: "Publication par entreprises ou banques des risques climatiques, émissions et dispositifs de gestion.", use: "Sans divulgation, les banques évaluent mal les risques physiques et de transition des clients." }, ar: { plain: "نشر الشركات أو البنوك لمخاطر المناخ والانبعاثات وإجراءات الإدارة.", use: "بدون الإفصاح يصعب على البنوك تقييم مخاطر الانتقال والمخاطر المادية لدى العملاء." }, zh: { plain: "企业或银行公开气候风险、排放和管理措施。", use: "没有披露，银行很难评估客户的转型风险和物理风险。" } } },
    { id: "Participatory finance", category: "new-finance", terms: { en: "Participatory finance", fr: "Finance participative", ar: "التمويل التشاركي", zh: "参与式金融" }, notes: { en: { plain: "Moroccan term for banking and finance products aligned with Islamic-finance principles.", use: "The question is whether it widens inclusion or remains a product line inside conventional banks." }, fr: { plain: "Terme marocain pour les banques et produits conformes aux principes de la finance islamique.", use: "La question est de savoir si elle élargit l'inclusion ou reste une ligne de produits bancaire." }, ar: { plain: "مصطلح مغربي للمنتجات والبنوك المتوافقة مع مبادئ المالية الإسلامية.", use: "السؤال هو هل يوسع الشمول المالي أم يبقى خط منتجات داخل البنوك التقليدية." }, zh: { plain: "摩洛哥语境中指符合伊斯兰金融原则的银行和金融产品。", use: "关键是它是否扩大金融包容性，还是只是传统银行内的一条产品线。" } } },
    { id: "Murabaha", category: "new-finance", terms: { en: "Murabaha", fr: "Mourabaha", ar: "مرابحة", zh: "成本加成销售融资" }, notes: { en: { plain: "A transaction where the bank buys an asset and resells it to the client with a known margin.", use: "Common in participatory finance for housing, equipment, or consumer finance." }, fr: { plain: "Opération où la banque achète un actif puis le revend au client avec une marge connue.", use: "Produit fréquent pour logement, équipement ou consommation en finance participative." }, ar: { plain: "عملية يشتري فيها البنك أصلا ثم يبيعه للعميل بهامش ربح معلوم.", use: "منتج شائع في التمويل التشاركي للسكن أو التجهيز أو الاستهلاك." }, zh: { plain: "银行先购买资产，再按已知利润加价卖给客户。", use: "参与式金融中常用于住房、设备或消费融资。" } } },
    { id: "Sukuk", category: "new-finance", terms: { en: "Sukuk", fr: "Sukuk", ar: "صكوك", zh: "伊斯兰债券" }, notes: { en: { plain: "Islamic financial certificates backed by assets or income rights, often compared to bonds.", use: "Can help governments or firms raise long-term participatory finance." }, fr: { plain: "Titres financiers islamiques adossés à des actifs ou revenus, souvent comparés à des obligations.", use: "Peuvent aider États ou entreprises à lever des financements longs." }, ar: { plain: "أوراق مالية إسلامية مدعومة بأصول أو حقوق دخل، وغالبا ما تقارن بالسندات.", use: "قد تساعد الحكومات أو الشركات على جمع تمويل طويل الأمد." }, zh: { plain: "以资产或收益权为支撑的伊斯兰金融证券，常与债券比较。", use: "可帮助政府或企业在参与式框架下筹集长期资金。" } } },
    { id: "Financial inclusion", category: "new-finance", terms: { en: "Financial inclusion", fr: "Inclusion financière", ar: "الشمول المالي", zh: "金融包容性" }, notes: { en: { plain: "Affordable access to formal financial services for individuals, small firms, and vulnerable groups.", use: "Often a policy goal in participatory finance, fintech, and SME financing." }, fr: { plain: "Accès abordable aux services financiers formels pour particuliers, petites entreprises et groupes vulnérables.", use: "Objectif fréquent dans finance participative, fintech et financement des PME." }, ar: { plain: "وصول ميسر إلى الخدمات المالية الرسمية للأفراد والمقاولات الصغيرة والفئات الهشة.", use: "هدف سياسي متكرر في التمويل التشاركي والتكنولوجيا المالية وتمويل المقاولات الصغرى والمتوسطة." }, zh: { plain: "让个人、小企业和弱势群体能负担并使用正规金融服务。", use: "参与式金融、金融科技和中小企业融资中常见的政策目标。" } } },
    { id: "Embedded finance", category: "new-finance", terms: { en: "Embedded finance", fr: "Finance embarquée", ar: "التمويل المدمج", zh: "嵌入式金融" }, notes: { en: { plain: "Payment, credit, or insurance services embedded inside non-financial platforms or user journeys.", use: "Asks whether the bank becomes a platform feature or keeps client access." }, fr: { plain: "Services de paiement, crédit ou assurance intégrés dans des plateformes ou parcours non financiers.", use: "Demande si la banque devient une fonctionnalité de plateforme ou conserve l'accès client." }, ar: { plain: "خدمات دفع أو ائتمان أو تأمين مدمجة داخل منصات أو مسارات غير مالية.", use: "تطرح سؤالا: هل يصبح البنك وظيفة داخل منصة أم يحتفظ بالوصول إلى العميل؟" }, zh: { plain: "把支付、信贷或保险嵌入非金融平台或业务场景。", use: "关注银行会变成平台功能，还是继续控制客户入口。" } } },
    { id: "Open banking", category: "new-finance", terms: { en: "Open banking", fr: "Open banking", ar: "الخدمات المصرفية المفتوحة", zh: "开放银行" }, notes: { en: { plain: "A framework where authorized third parties access bank data or services through secure interfaces.", use: "Can change credit scoring, payments, and product distribution." }, fr: { plain: "Cadre où des tiers autorisés accèdent aux données ou services bancaires via interfaces sécurisées.", use: "Peut modifier l'évaluation du crédit, les paiements et la distribution." }, ar: { plain: "إطار يسمح لأطراف مرخصة بالوصول إلى بيانات أو خدمات بنكية عبر واجهات آمنة.", use: "قد يغير تقييم الائتمان والمدفوعات وتوزيع المنتجات." }, zh: { plain: "在授权和监管下，让第三方通过安全接口使用银行数据或服务。", use: "可能改变信贷评估、支付服务和金融产品分发。" } } },
    { id: "Banking as a Service", category: "new-finance", terms: { en: "Banking as a Service (BaaS)", fr: "Banque en tant que service", ar: "الخدمات البنكية كخدمة", zh: "银行即服务" }, notes: { en: { plain: "Bank accounts, payments, compliance, or credit capabilities exposed to other platforms through APIs.", use: "Explains why non-bank platforms can become finance entry points." }, fr: { plain: "Comptes, paiements, conformité ou crédit fournis par une banque à d'autres plateformes via API.", use: "Explique pourquoi des plateformes non bancaires deviennent des points d'entrée financiers." }, ar: { plain: "حسابات ومدفوعات وامتثال أو قدرات ائتمان يقدمها البنك لمنصات أخرى عبر واجهات برمجة.", use: "يفسر كيف تصبح منصات غير بنكية مداخل إلى التمويل." }, zh: { plain: "银行通过接口向其他平台提供账户、支付、合规或信贷能力。", use: "解释为什么非银行平台也可能成为金融入口。" } } },
    { id: "Development finance", category: "capital", terms: { en: "Development finance", fr: "Finance de développement", ar: "تمويل التنمية", zh: "发展金融" }, notes: { en: { plain: "Public or multilateral finance using loans, guarantees, or equity to support development goals.", use: "U.S. DFC influence in Morocco is closer to this than to commercial banking networks." }, fr: { plain: "Financement public ou multilatéral par prêts, garanties ou participations pour soutenir le développement.", use: "L'influence de la DFC au Maroc relève davantage de ce canal que de banques commerciales." }, ar: { plain: "تمويل عام أو متعدد الأطراف يستخدم القروض أو الضمانات أو المساهمات لدعم أهداف التنمية.", use: "تأثير DFC الأمريكية في المغرب أقرب إلى هذا المسار من شبكات البنوك التجارية." }, zh: { plain: "政府或多边机构用贷款、担保或股权支持发展目标的金融活动。", use: "美国 DFC 在摩洛哥的影响更接近发展金融，而非商业银行网络。" } } },
    { id: "Foreign direct investment", category: "capital", terms: { en: "Foreign direct investment (FDI)", fr: "Investissement direct étranger", ar: "الاستثمار الأجنبي المباشر", zh: "外国直接投资" }, notes: { en: { plain: "Long-term foreign investment in a company, factory, project, or equity stake.", use: "Must be distinguished from loans, guarantees, trade finance, and portfolio flows." }, fr: { plain: "Investissement étranger durable dans une entreprise, usine, projet ou participation au capital.", use: "À distinguer des prêts, garanties, financements du commerce et flux de portefeuille." }, ar: { plain: "استثمار أجنبي طويل الأجل في شركة أو مصنع أو مشروع أو حصة رأسمالية.", use: "يجب تمييزه عن القروض والضمانات وتمويل التجارة وتدفقات المحافظ." }, zh: { plain: "外国投资者在企业、工厂、项目或股权中进行的长期投资。", use: "需要与贷款、担保、贸易融资和证券投资区分开。" } } },
    { id: "Capital flows", category: "capital", terms: { en: "Capital flows", fr: "Flux de capitaux", ar: "تدفقات رأس المال", zh: "资本流动" }, notes: { en: { plain: "Movements of funds between countries, markets, and institutions.", use: "A common frame for comparing Chinese capital, U.S. development finance, and European banking shifts." }, fr: { plain: "Mouvements de fonds entre pays, marchés et institutions.", use: "Cadre commun pour comparer capitaux chinois, finance américaine de développement et banques européennes." }, ar: { plain: "حركات الأموال بين الدول والأسواق والمؤسسات.", use: "إطار مشترك لمقارنة رأس المال الصيني وتمويل التنمية الأمريكي وتحولات البنوك الأوروبية." }, zh: { plain: "资金在国家、市场和机构之间的流入流出。", use: "可用于比较中国资本、美国发展金融和欧洲银行变化。" } } },
    { id: "Value chain", category: "capital", terms: { en: "Value chain", fr: "Chaîne de valeur", ar: "سلسلة القيمة", zh: "价值链" }, notes: { en: { plain: "The sequence from raw materials and components to production, logistics, and sales.", use: "Chinese investment in energy, minerals, and autos often follows value-chain logic." }, fr: { plain: "Séquence allant des matières premières et composants à la production, logistique et vente.", use: "Les investissements chinois dans énergie, minerais et automobile suivent souvent cette logique." }, ar: { plain: "تسلسل من المواد الخام والمكونات إلى الإنتاج واللوجستيك والبيع.", use: "الاستثمارات الصينية في الطاقة والمعادن والسيارات غالبا ما تتبع منطق سلسلة القيمة." }, zh: { plain: "从原材料、零部件到生产、物流和销售的完整链条。", use: "中国在能源、矿产和汽车领域的投资常体现价值链布局。" } } },
    { id: "Strategic minerals", category: "capital", terms: { en: "Strategic minerals", fr: "Minéraux stratégiques", ar: "المعادن الاستراتيجية", zh: "战略矿产" }, notes: { en: { plain: "Minerals considered critical for energy transition, industrial security, or supply chains.", use: "Links batteries, electric vehicles, energy, and geoeconomic competition." }, fr: { plain: "Minéraux jugés critiques pour la transition énergétique, la sécurité industrielle ou les chaînes d'approvisionnement.", use: "Relient batteries, véhicules électriques, énergie et concurrence géoéconomique." }, ar: { plain: "معادن تعتبر حاسمة للانتقال الطاقي أو الأمن الصناعي أو سلاسل الإمداد.", use: "تربط البطاريات والمركبات الكهربائية والطاقة والمنافسة الجيو اقتصادية." }, zh: { plain: "对能源转型、工业安全或供应链具有关键意义的矿产。", use: "连接电池、电动车、能源和地缘经济竞争。" } } },
    { id: "Infrastructure finance", category: "capital", terms: { en: "Infrastructure finance", fr: "Financement des infrastructures", ar: "تمويل البنية التحتية", zh: "基础设施融资" }, notes: { en: { plain: "Long-term finance for ports, railways, roads, energy, water, or industrial zones.", use: "A starting point for early Chinese capital, development institutions, and public projects." }, fr: { plain: "Financement de long terme pour ports, chemins de fer, routes, énergie, eau ou zones industrielles.", use: "Point d'entrée pour capitaux chinois initiaux, institutions de développement et projets publics." }, ar: { plain: "تمويل طويل الأجل للموانئ والسكك والطرق والطاقة والماء والمناطق الصناعية.", use: "مدخل لفهم رأس المال الصيني الأولي ومؤسسات التنمية والمشاريع العمومية." }, zh: { plain: "为港口、铁路、公路、能源、水利或工业园区提供的长期融资。", use: "理解早期中国资本、发展机构和公共项目的入口。" } } }
  ]
};
