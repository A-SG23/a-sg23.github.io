/* Every project on the portfolio page lives here.
   Adding a project = adding one object to this array. Nothing else to touch.

   slug        used for the window filename and as a stable id
   name        display name, rendered verbatim (casing is preserved)
   tagline     one line under the name
   status      free text, e.g. "live for users" / "shipped" / "in development"
   tags        2-3 technologies
   description shown on hover (desktop) or inline (touch)
   icon        16px pixel icon for the title bar
   cover       art for the card's image area
   links       first non-null of live / writeup / repo becomes the card's href;
               a project with no links renders as a non-clicking card
*/
window.PROJECTS = [
  {
    slug: "minus",
    name: "minus.",
    file: "minus.exe",
    tagline: "personalized petite fitting tool",
    status: "live for users",
    tags: ["TypeScript", "SVG"],
    description:
      "petite sizing is guesswork. this renders your actual proportions " +
      "against real brand size charts so you can see fit before you buy.",
    icon: "assets/img/icon-shirt.png",
    cover: "assets/img/cover-minus.png",
    links: {
      live: "https://minus-size.vercel.app/",
      repo: null,
      writeup: null,
    },
  },
  {
    slug: "safenest",
    name: "safenest",
    file: "safenest.exe",
    tagline: "mobile app · 1st @ cgu hacks",
    status: "shipped",
    tags: ["React", "MindStudio", "ArcGIS"],
    description:
      "a hub for expectant mothers. includes ArcGIS-powered environmental " +
      "risk-mapping, agent for medical document interpretation, agent for " +
      "prenatal care-specific clinic search, and a community forum for " +
      "current and soon-to-be mothers. built in 12 hours with a team of 4.",
    icon: "assets/img/icon-baby.png",
    cover: "assets/img/cover-safenest.png",
    links: { live: null, repo: null, writeup: null },
  },
  {
    slug: "aeye",
    name: "aEye",
    file: "aEye.exe",
    tagline: "eyeliner enthusiast hub",
    status: "in development",
    tags: ["TypeScript", "MediaPipe", "Canvas"],
    description:
      "faces aren't symmetric, so \"is my eyeliner even?\" needs to be " +
      "meticulously mapped. writing the spec before the code.",
    icon: "assets/img/icon-eye.png",
    cover: "assets/img/cover-aeye.png",
    links: { live: null, repo: null, writeup: null },
  },
];
