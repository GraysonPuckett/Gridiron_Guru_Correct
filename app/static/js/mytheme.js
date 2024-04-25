const themes = {
    "Cardinals": {"primary": "#FFFFFF", "secondary": "#97233F", "footer": "#97233F", "navbarText": "#000000"},
    "Falcons": {"primary": "#A71930", "secondary": "#FFFFFF", "footer": "#000000", "navbarText": "#000000"},
    "Ravens": {"primary": "#FFFFFF", "secondary": "#24135F", "footer": "#24135F", "navbarText": "#FFFFFF"},
    "Bills": {"primary": "#C60C30", "secondary": "#FFFFFF", "footer": "#00338D", "navbarText": "#000000"},
    "Panthers": {"primary": "#0085CA", "secondary": "#FFFFFF", "footer": "#000000", "navbarText": "#000000"},
    "Bears": {"primary": "#E64100", "secondary": "#FFFFFF", "footer": "#0B162A", "navbarText": "#000000"},
    "Bengals": {"primary": "#FB4F14", "secondary": "#FFFFFF", "footer": "#000000", "navbarText": "#000000"},
    "Browns": {"primary": "#FF3300", "secondary": "#FFFFFF", "footer": "#311D00", "navbarText": "#000000"},
    "Cowboys": {"primary": "#B0B7BC", "secondary": "#002244", "footer": "#002244", "navbarText": "#FFFFFF"},
    "Broncos": {"primary": "#FC4C02", "secondary": "#0A2343", "footer": "#FC4C02", "navbarText": "#FFFFFF"},
    "Lions": {"primary": "#B0B7BC", "secondary": "#0076B6", "footer": "#0076B6", "navbarText": "#000000"},
    "Packers": {"primary": "#FFB612", "secondary": "#203731", "footer": "#203731", "navbarText": "#FFFFFF"},
    "Texans": {"primary": "#A71930", "secondary": "#03202F", "footer": "#03202F", "navbarText": "#FFFFFF"},
    "Colts": {"primary": "#FFFFFF", "secondary": "#003A70", "footer": "#003A70", "navbarText": "#FFFFFF"},
    "Jaguars": {"primary": "#FFFFFF", "secondary": "#006778", "footer": "#006778", "navbarText": "#000000"},
    "Chiefs": {"primary": "#E31837", "secondary": "#FFB612", "footer": "#E31837", "navbarText": "#000000"},
    "Chargers": {"primary": "#0080C6", "secondary": "#FFC20E", "footer": "#0080C6", "navbarText": "#000000"},
    "Rams": {"primary": "#003594", "secondary": "#FFD100", "footer": "#003594", "navbarText": "#000000"},
    "Dolphins": {"primary": "#008E97", "secondary": "#FC4C02", "footer": "#008E97", "navbarText": "#000000"},
    "Vikings": {"primary": "#4F2683", "secondary": "#FFC62F", "footer": "#4F2683", "navbarText": "#000000"},
    "Patriots": {"primary": "#002244", "secondary": "#C60C30", "footer": "#002244", "navbarText": "#000000"},
    "Saints": {"primary": "#D3BC8D", "secondary": "#000000", "footer": "#D3BC8D", "navbarText": "#FFFFFF"},
    "Giants": {"primary": "#0B2265", "secondary": "#A71930", "footer": "#0B2265", "navbarText": "#000000"},
    "Jets": {"primary": "#125740", "secondary": "#FFFFFF", "footer": "#125740", "navbarText": "#000000"},
    "Eagles": {"primary": "#004C54", "secondary": "#A5ACAF", "footer": "#004C54", "navbarText": "#000000"},
    "Steelers": {"primary": "#FFB612", "secondary": "#000000", "footer": "#000000", "navbarText": "#FFFFFF"},
    "Seahawks": {"primary": "#69BE28", "secondary": "#002244", "footer": "#002244", "navbarText": "#FFFFFF"},
    "49ers": {"primary": "#AA0000", "secondary": "#B3995D", "footer": "#AA0000", "navbarText": "#000000"},
    "Buccaneers": {"primary": "#D50A0A", "secondary": "#34302B", "footer": "#D50A0A", "navbarText": "#ffffff"},
    "Titans": {"primary": "#0C2340", "secondary": "#4B92DB", "footer": "#0C2340", "navbarText": "#000000"},
    "Commanders": {"primary": "#773141", "secondary": "#FFB612", "footer": "#773141", "navbarText": "#000000"},
    "Raiders": {"primary": "#A5ACAF", "secondary": "#000000", "footer": "#000000", "navbarText": "#FFFFFF"},
};


function applyTheme(themeKey) {
    const theme = themes[themeKey];
    if (!theme) return;

    // Apply primary and secondary colors
    document.documentElement.style.setProperty('--primary-color', theme.primary);
    document.documentElement.style.setProperty('--secondary-color', theme.secondary);

    // Teams requiring white navbar and footer text
    const teamsWhiteText = ["Broncos", "Buccaneers", "Colts", "Cowboys", "Packers", "Raiders", "Ravens", "Saints", "Seahawks", "Steelers", "Texans", "Commanders", "Eagles", "49ers", "Giants", "Patriots", "Rams", "Titans", "Vikings"];

    // Determine the correct text color for navbar, footer, and body
    let textColor = teamsWhiteText.includes(themeKey) ? "#FFFFFF" : "#000000";

    // Apply text colors
    document.documentElement.style.setProperty('--navbar-text-color', textColor);
    document.documentElement.style.setProperty('--text-color', textColor); // Body text color
    document.documentElement.style.setProperty('--footer-text-color', textColor); // Footer text color

    // Apply footer and navbar background color
    // For semi-transparent footer, consider using RGBA color format or a semi-transparent HEX color.
    document.documentElement.style.setProperty('--footer-background-color', theme.footer + '7D'); // Adding '7D' for 49% opacity in HEX
    document.documentElement.style.setProperty('--navbar-background-color', theme.primary); // or theme.secondary, depending on your design
}

document.addEventListener('DOMContentLoaded', () => {
    const themeSelector = document.getElementById('theme-selector');
    const savedTheme = localStorage.getItem('selectedTheme');

    if (savedTheme && themes[savedTheme]) {
        applyTheme(savedTheme);
        if (themeSelector) {
            themeSelector.value = savedTheme;
        }
    }

    if (themeSelector) {
        themeSelector.addEventListener('change', function() {
            const selectedTheme = this.value;
            localStorage.setItem('selectedTheme', selectedTheme);
            applyTheme(selectedTheme);
        });
    }
});