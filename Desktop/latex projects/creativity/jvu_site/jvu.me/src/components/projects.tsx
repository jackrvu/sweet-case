import React from 'react';

// Define the structure for a project
interface Project {
  name: string;
  description: string;
  links: {
    github?: string;
    site?: string;
    paper?: string;
    prezi?: string;
    writeup?: string;
  };
}

// Your projects data
const projects: Project[] = [
  {
    name: "mav hub ios app",
    description: "school app that displays all schedule, club, and assignment information. 110k uses/mo, 1.1k regular users.",
    links: {
      site: "https://apps.apple.com/bf/app/mav-hub/id6670142459"
    }

    },
    {
      name: "image face autotagger (like instagram)",
      description: "scrapes student & faculty directory, uses insightface for face recognition. software donated to school yearbook.",
      links: {
        github: "https://github.com/jackrvu/face_req"
      }
      },
    {
    name: "spanish dialect classifier",
    description: "bag-of-words model trained on reddit posts from spanish-speaking countries",
    links: {
      github: "https://github.com/jackrvu/clasificador-cervantes"
    }
    },
    {
    name: "python curriculum for elementary students",
    description: "for use in a summer camp at mission milby in east houston.",
    links: {
      github: "https://github.com/jackrvu/python-easy"
    }
    },
    {
    name: "backwards citation search for company patents",
    description: "scrapes u.s. patent office website to create a full company patent citation ranking.",
    links: {
      github: "https://github.com/jackrvu/sweet-case"
    }
    },
    {
    name: "scrabble point-maximizing algorithm w/ basic interface",
    description: "implementation of 'The World's Fastest Scrabble Program' (appel, jacobson).",
    links: {
      github: "https://github.com/jackrvu/scrabble-maverick"
    }
    },
    {
    name: "bot for defeating the jklm bomb party game",
    description: "algorithmic word generation w/ live html scraping, simulates inputs to site.",
    links: {
      github: "https://github.com/jackrvu/word-wizard"
    }
    },
    {
    name: "spanish-language digital literacy curriculum",
    description: "for use in a course at the st. austin center in east houston.",
    links: {
      github: "https://github.com/jackrvu/the-digital-doorway"
    }
    },
    {
    name: "optimizing wordle play",
    description: "min-max approach to word list reduction and effective guess selection.",
    links: {
      github: "https://github.com/jackrvu/min-wordle"
    }
  }
];

const ProjectsList: React.FC = () => {
    return (
      <div className="space-y-3">
        {projects.map((project, index) => (
          <div key={index} className="pb-2">
            <h3 className="text-3xs lg:text-2xs font-bold">{project.name}</h3>
            <p className="text-3xs lg:text-2xs text-gray-600">{project.description}</p>
            <div className="flex flex-wrap gap-2 text-3xs lg:text-2xs">
              {project.links.github && (
                <a href={project.links.github} className="text-blue-600 hover:text-blue-800 transition-colors duration-200" target="_blank" rel="noopener noreferrer">GitHub</a>
              )}
              {project.links.site && (
                <a href={project.links.site} className="text-purple-600 hover:text-purple-800 transition-colors duration-200" target="_blank" rel="noopener noreferrer">Website</a>
              )}
              {project.links.paper && (
                <a href={project.links.paper} className="text-orange-600 hover:text-orange-800 transition-colors duration-200" target="_blank" rel="noopener noreferrer">Paper</a>
              )}
              {project.links.prezi && (
                <a href={project.links.prezi} className="text-green-600 hover:text-green-800 transition-colors duration-200" target="_blank" rel="noopener noreferrer">Prezi</a>
              )}
              {project.links.writeup && (
                <a href={project.links.writeup} className="text-pink-600 hover:text-pink-800 transition-colors duration-200" target="_blank" rel="noopener noreferrer">Writeup</a>
              )}
            </div>
          </div>
        ))}
      </div>
    );
};

export default ProjectsList;