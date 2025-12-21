document.addEventListener('DOMContentLoaded', () => {
    // --- Elements ---
    const setupScreen = document.getElementById('setup-screen');
    const appContainer = document.getElementById('app-container');
    const folderInput = document.getElementById('folder-input');
    const municipalityList = document.getElementById('municipality-list');
    const pageTitle = document.getElementById('page-title');
    const placeholder = document.getElementById('placeholder-message');
    const reportContainer = document.getElementById('report-container');
    const contentOverview = document.getElementById('content-overview');
    const contentDetails = document.getElementById('content-details');
    const backToTopBtn = document.getElementById('back-to-top');
    const sidebar = document.querySelector('.sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');

    // --- State ---
    // Structure: { "GemeenteNaam": { "file.md": FileObject|String, ... } }
    let municipalityData = {};

    // List of files to load for the details view (in order)
    const detailFilesOrder = [
        '00_zondag_kerkelijk_jaar.md',
        '01_sociaal_maatschappelijke_context.md',
        '02_waardenorientatie.md',
        '03_geloofsorientatie.md',
        '04_interpretatieve_synthese.md',
        '05_actueel_wereldnieuws.md',
        '06_politieke_orientatie.md',
        '07_exegese.md',
        '08_kunst_cultuur.md',
        '09_focus_en_functie.md',
        '10_kalender.md',
        '11_representatieve_hoorders.md',
        '12_homiletische_analyse.md',
        '13_gebeden.md'
    ];

    // Readable labels for section menu
    const sectionLabels = {
        '00_zondag_kerkelijk_jaar.md': 'Zondag & Kerkelijk Jaar',
        '01_sociaal_maatschappelijke_context.md': 'Sociaal-Maatschappelijk',
        '02_waardenorientatie.md': 'Waardenoriëntatie',
        '03_geloofsorientatie.md': 'Geloofsoriëntatie',
        '04_interpretatieve_synthese.md': 'Interpretatieve Synthese',
        '05_actueel_wereldnieuws.md': 'Actueel Wereldnieuws',
        '06_politieke_orientatie.md': 'Politieke Oriëntatie',
        '07_exegese.md': 'Exegese',
        '08_kunst_cultuur.md': 'Kunst & Cultuur',
        '09_focus_en_functie.md': 'Focus & Functie',
        '10_kalender.md': 'Kalender',
        '11_representatieve_hoorders.md': 'Representatieve Hoorders',
        '12_homiletische_analyse.md': 'Homiletische Analyse',
        '13_gebeden.md': 'Gebeden'
    };

    // Current active municipality for submenu
    let currentMunicipality = null;

    // --- Helpers ---
    function formatName(name) {
        return name.replace(/_/g, ' ');
    }

    function smartQuotes(text) {
        return text
            // Double quotes
            .replace(/(^|[-\u2014\s(\[{"'])"/g, '$1\u201c') // opening
            .replace(/"/g, '\u201d')                         // closing
            // Single quotes / apostrophes
            .replace(/(^|[-\u2014\s(\[{"'])'/g, '$1\u2018') // opening
            .replace(/'/g, '\u2019');                        // closing
    }

    // Fix relative links to point to the correct subdirectory
    function fixRelativeLinks(container, dirName) {
        const links = container.querySelectorAll('a');
        links.forEach(link => {
            const href = link.getAttribute('href');
            // Check if it's a relative link to a markdown file
            if (href && !href.startsWith('http') && !href.startsWith('/') && !href.startsWith('#') && href.endsWith('.md')) {
                link.setAttribute('href', `${dirName}/${href}`);
            }
        });
    }

    // Helper to read a File object as text or return string if already text
    function getFileContent(fileOrString) {
        if (typeof fileOrString === 'string') {
            return Promise.resolve(fileOrString);
        }
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = e => resolve(e.target.result);
            reader.onerror = e => reject(e);
            reader.readAsText(fileOrString);
        });
    }

    // --- Initialization ---
    function init() {
        if (window.CONTEXT_DATA) {
            municipalityData = window.CONTEXT_DATA;
            renderSidebar();
            setupScreen.classList.add('hidden');
            appContainer.classList.remove('hidden');
        }
    }

    // --- Event Listeners ---

    // 1. Handle Folder Selection
    folderInput.addEventListener('change', (event) => {
        const files = event.target.files;
        if (!files || files.length === 0) return;

        municipalityData = {}; // Reset

        // Process files
        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            const parts = file.webkitRelativePath.split('/');
            
            if (parts.length < 2) continue;

            const fileName = parts[parts.length - 1];
            const dirName = parts[parts.length - 2];

            if (dirName.startsWith('.') || dirName === 'css' || dirName === 'js' || dirName === 'output') continue;
            if (['index.html', 'script.js', 'style.css', 'website_server.py', 'data.js', 'generate_data.py'].includes(fileName)) continue;
            if (!fileName.endsWith('.md')) continue;

            if (!municipalityData[dirName]) {
                municipalityData[dirName] = {};
            }
            municipalityData[dirName][fileName] = file;
        }

        renderSidebar();
        setupScreen.classList.add('hidden');
        appContainer.classList.remove('hidden');
    });

    // 2. Render Sidebar
    function renderSidebar() {
        municipalityList.innerHTML = '';
        const dirs = Object.keys(municipalityData).sort();

        if (dirs.length === 0) {
            municipalityList.innerHTML = '<li style="padding:20px; color:#999;">Geen geldige mappen gevonden.</li>';
            return;
        }

        dirs.forEach(dir => {
            const li = document.createElement('li');
            li.className = 'municipality-item';
            li.dataset.dir = dir;

            const btn = document.createElement('button');
            btn.className = 'municipality-btn';
            btn.textContent = formatName(dir);
            btn.onclick = () => loadReport(dir, li);
            li.appendChild(btn);

            // Create submenu container
            const submenu = document.createElement('ul');
            submenu.className = 'section-submenu';

            // Add submenu items for each available section
            const filesMap = municipalityData[dir];
            detailFilesOrder.forEach(filename => {
                if (filesMap[filename]) {
                    const subLi = document.createElement('li');
                    const subBtn = document.createElement('button');
                    subBtn.className = 'section-btn';
                    subBtn.dataset.section = filename;
                    subBtn.textContent = sectionLabels[filename] || filename;
                    subBtn.onclick = (e) => {
                        e.stopPropagation();
                        scrollToSection(filename);
                    };
                    subLi.appendChild(subBtn);
                    submenu.appendChild(subLi);
                }
            });

            li.appendChild(submenu);
            municipalityList.appendChild(li);
        });
    }

    // Scroll to a specific section
    function scrollToSection(filename) {
        const targetSection = document.getElementById(`section-${filename}`);
        if (targetSection) {
            targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            // Collapse sidebar on mobile after selecting a section
            if (isMobile()) {
                setTimeout(() => collapseSidebar(), 300);
            }
        }
    }

    // Check if mobile (defined early for use in scrollToSection)
    function isMobile() {
        return window.innerWidth <= 768;
    }

    // Update active section in submenu based on scroll position
    function updateActiveSection() {
        if (!currentMunicipality) return;

        const sections = contentDetails.querySelectorAll('.file-section');
        const containerRect = reportContainer.getBoundingClientRect();
        const containerTop = containerRect.top;

        let activeSection = null;

        sections.forEach(section => {
            const rect = section.getBoundingClientRect();
            // Check if section is at or near the top of the viewport
            if (rect.top <= containerTop + 150) {
                activeSection = section.dataset.file;
            }
        });

        // Update submenu buttons
        const submenuBtns = document.querySelectorAll('.section-btn');
        submenuBtns.forEach(btn => {
            if (btn.dataset.section === activeSection) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }

    // 3. Load Report Logic
    async function loadReport(dirName, liElement) {
        // UI Update - remove active from all municipality items
        document.querySelectorAll('.municipality-item').forEach(item => {
            item.classList.remove('active');
            item.querySelector('.municipality-btn').classList.remove('active');
        });

        // Mark current municipality as active
        liElement.classList.add('active');
        liElement.querySelector('.municipality-btn').classList.add('active');
        currentMunicipality = dirName;

        // Update toggle button text on mobile
        updateToggleButtonText();
        
        pageTitle.textContent = formatName(dirName);
        placeholder.classList.add('hidden');
        reportContainer.classList.remove('hidden');

        // Scroll to top of report container
        reportContainer.scrollTop = 0;
        // Hide FAB initially
        backToTopBtn.classList.remove('visible');

        // Reset content
        contentOverview.innerHTML = '<p>Laden...</p>';
        contentDetails.innerHTML = '';

        const filesMap = municipalityData[dirName];

        // --- Load Overview ---
        if (filesMap['00_overzicht.md']) {
            try {
                const text = await getFileContent(filesMap['00_overzicht.md']);
                contentOverview.innerHTML = marked.parse(smartQuotes(text));
                fixRelativeLinks(contentOverview, dirName);
            } catch (e) {
                console.error(e);
                contentOverview.innerHTML = '<p>Fout bij laden overzicht.</p>';
            }
        } else {
            contentOverview.innerHTML = '<p><em>Geen overzicht beschikbaar.</em></p>';
        }

        // --- Load Details ---
        let detailsHtml = '';
        
        for (const filename of detailFilesOrder) {
            if (filesMap[filename]) {
                try {
                    const text = await getFileContent(filesMap[filename]);
                    
                    detailsHtml += `<div class="section-divider"></div>`;
                    // Note: Removed the injected button here
                    detailsHtml += `<div class="file-section" id="section-${filename}" data-file="${filename}">`;
                    detailsHtml += marked.parse(smartQuotes(text));
                    detailsHtml += `</div>`;
                } catch (e) {
                    console.warn(`Could not load ${filename}`, e);
                }
            }
        }

        contentDetails.innerHTML = detailsHtml;
        fixRelativeLinks(contentDetails, dirName);
    }

    // --- Link Handling ---
    document.body.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        if (!link) return;

        const href = link.getAttribute('href');
        // Check if it's an internal MD link
        if (href && href.endsWith('.md')) {
            e.preventDefault();
            
            const filename = href.split('/').pop();
            const targetSection = document.getElementById(`section-${filename}`);
            
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
                console.warn(`Section for ${filename} not found.`);
            }
        }
    });

    const mainHeader = document.querySelector('.main-header');

    // --- Mobile Sidebar Collapse ---
    let lastScrollTop = 0;

    function collapseSidebar() {
        if (isMobile() && currentMunicipality) {
            sidebar.classList.add('collapsed');
            updateToggleButtonText();
        }
    }

    function expandSidebar() {
        sidebar.classList.remove('collapsed');
    }

    function updateToggleButtonText() {
        if (currentMunicipality) {
            sidebarToggle.innerHTML = `${formatName(currentMunicipality)} <span class="toggle-icon">▼</span>`;
        } else {
            sidebarToggle.innerHTML = `Menu openen <span class="toggle-icon">▼</span>`;
        }
    }

    // Toggle button click handler
    sidebarToggle.addEventListener('click', () => {
        if (sidebar.classList.contains('collapsed')) {
            expandSidebar();
        } else {
            collapseSidebar();
        }
    });

    // --- FAB Handling ---
    // Scroll listener on the report container
    reportContainer.addEventListener('scroll', () => {
        const scrollTop = reportContainer.scrollTop;

        // FAB visibility
        if (scrollTop > 300) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }

        // Header shrinking
        if (scrollTop > 50) {
            mainHeader.classList.add('scrolled');
        } else {
            mainHeader.classList.remove('scrolled');
        }

        // Auto-collapse sidebar on mobile when scrolling down
        if (isMobile() && currentMunicipality) {
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                collapseSidebar();
            }
            lastScrollTop = scrollTop;
        }

        // Update active section in submenu
        updateActiveSection();
    });

    // Click listener for FAB
    backToTopBtn.addEventListener('click', () => {
        reportContainer.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // --- Font Size Controls ---
    const fontDecrease = document.getElementById('font-decrease');
    const fontIncrease = document.getElementById('font-increase');
    const markdownBody = document.querySelectorAll('.markdown-body');

    // Base font size in rem
    let currentFontSize = parseFloat(localStorage.getItem('fontSize')) || 1.1;
    const minFontSize = 0.8;
    const maxFontSize = 1.6;
    const fontStep = 0.1;

    function updateFontSize() {
        document.documentElement.style.setProperty('--content-font-size', currentFontSize + 'rem');
        // Apply to all markdown bodies
        document.querySelectorAll('.markdown-body').forEach(el => {
            el.style.fontSize = currentFontSize + 'rem';
        });
        localStorage.setItem('fontSize', currentFontSize);
    }

    // Apply saved font size on load
    updateFontSize();

    fontDecrease.addEventListener('click', () => {
        if (currentFontSize > minFontSize) {
            currentFontSize = Math.round((currentFontSize - fontStep) * 10) / 10;
            updateFontSize();
        }
    });

    fontIncrease.addEventListener('click', () => {
        if (currentFontSize < maxFontSize) {
            currentFontSize = Math.round((currentFontSize + fontStep) * 10) / 10;
            updateFontSize();
        }
    });

    // Run Init
    init();
});
