from django.core.management.base import BaseCommand
from home.models import ContentType, Repository, Area

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        self._create_content_types()
        self._create_repositories()
        self._create_areas()
        self.stdout.write('Data seeded successfully.')

    def _create_content_types(self):
        content_type_data = [
            "Almanaque",
            "Anuario",
            "Apuntes",
            "Artículo Cultural",
            "Artículo de Divulgación",
            "Artículo de Investigación",
            "Artículo Preliminar",
            "Artículo Técnico-Profesional",
            "Avance de Investigación",
            "Boletín",
            "Capítulo de Libro",
            "Capítulo de Memoria de Congreso",
            "Cápsula Educativa",
            "Cápsula Informativa",
            "Ceremonia",
            "Curso",
            "Diapositivas de Conferencia",
            "Diploma",
            "Directorio",
            "Documento de conferencia",
            "Entrevista",
            "Estatuto",
            "Folleto",
            "Foro-",
            "Infografía",
            "Informe Científico",
            "Informe de Actividades",
            "Informe de Investigación",
            "Instructivo",
            "Libro",
            "Manual",
            "Manuscrito",
            "Mapa",
            "Memorándum",
            "Memoria de Congreso",
            "Monografía",
            "Otro Material de Biblioteca",
            "Parte de Periódico",
            "Periódico",
            "Proyecto de Investigación",
            "Recopilación",
            "Registro de Archivo Personal",
            "Registro de Colección de Proyectos",
            "Reglamento",
            "Reseña",
            "Revista de Divulgación",
            "Tesis de Doctorado",
            "Tesis de Licenciatura",
            "Tesis de Maestría",
            "Trabajo de Grado a Nivel Técnico",
            "Trabajo de Grado de Especialización",

            # agregar los tipos de contenido aqui separadas por coma
        ]
        for content_type_name in content_type_data:
            ContentType.objects.create(name=content_type_name)

    def _create_repositories(self):
        repository_data = [
            "Academia",
            "Advances in Intelligent Systems and Computing",
            "Applied Sciences",
            "Autonomous Agents and Multi-Agent Systems",
            "Ciencias Marinas",
            "Conference: International Conference on Innovation in Medicine and Healthcare",
            "Editorial Académica Española",
            "Frontiers in Energy Research",
            "Fuzzy Sets and Systems",
            "Humanities & Social Sciences Reviews",
            "IEEE Computer Applications in Power",
            "In book: Agents and Multi-Agent Systems: Technologies and Applications 2018",
            "In book: Agents and Multi-agent Systems: Technologies and Applications 2019",
            "In book: Computer Science and Engineering—Theory and Applications.",
            "In book: Congreso Internacional en Ciencias Computacionales",
            "In book: Desarrollo de negocios internacionales a través de la gestión del conocimiento",
            "In book: Innovation in Medicine and Healthcare",
            "In book: International Conference on Information Society",
            "In book: New Knowledge in Information Systems and Technologies",
            "In book: Pymes: empresarial y social",
            "In book: Smart Innovation, Systems and Technologies",
            "In book: Towards a Social Simulator Based on Agents for Management of the Knowledge Base for the Strengthening of Learning Competences.",
            "In book: Towards Team Formation Using Belbin Role Types and a Social Networks Analysis Approach",
            "In book: Trends and Innovations in Information Systems and Technologies",
            "Innovaitescyt los cabos",
            "Otras Instituciones",
            "Revista Ciencias de la Complejidad 2",
            "Revista Ibérica de Sistemas e Tecnologias de Informaçã",
            "Revista de Investigación en Tecnologías de la Información",
            "Systems",
            "Towards Recommendation System for Work-group Formation Using Social Network Analysis Approach.",
            

            # agregar los repositorios aqui separadas por coma
        ]
        for repository_name in repository_data:
            Repository.objects.create(name=repository_name)

    def _create_areas(self):
        area_data = [
            "Artes y Humanidades",
            "Ciencias Computacionales",
            "Ciencias Sociales y Económicas",
            "Físico Matemáticas",
            "Ingenierías",
            "Innovación y Tecnología",
            "Medicina y Ciencias de la Salud",
            "Multidisciplina",
            # agregar las areas aqui separadas por coma
        ]
        for area_name in area_data:
            Area.objects.create(name=area_name)