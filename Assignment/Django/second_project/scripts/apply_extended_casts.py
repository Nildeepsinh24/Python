import os
import sys
import django

# Setup path and django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'second_project.settings')
django.setup()

from cine_verse.models import Movie

extended_casts = {
    "Spirited Away": "Rumi Hiiragi, Miyu Irino, Mari Natsuki, Takashi Naito, Yasuko Sawaguchi, Tatsuya Gashuin, Ryunosuke Kamiki, Yumi Tamai, Yo Oizumi, Koba Hayashi, Tsunehiko Kamijo",
    "Spider-Man": "Tom Holland, Zendaya, Benedict Cumberbatch, Jacob Batalon, Jon Favreau, Marisa Tomei, Jamie Foxx, Willem Dafoe, Alfred Molina, Andrew Garfield, Tobey Maguire, J.K. Simmons",
    "Breaking Bad": "Bryan Cranston, Aaron Paul, Anna Gunn, Dean Norris, Betsy Brandt, RJ Mitte, Bob Odenkirk, Giancarlo Esposito, Jonathan Banks, Jesse Plemons, Laura Fraser, Steven Michael Quezada",
    "The Lord of the Rings": "Elijah Wood, Ian McKellen, Liv Tyler, Viggo Mortensen, Sean Astin, Cate Blanchett, John Rhys-Davies, Bernard Hill, Christopher Lee, Billy Boyd, Dominic Monaghan, Orlando Bloom, Hugo Weaving, Sean Bean, Andy Serkis",
    "The Shining": "Jack Nicholson, Shelley Duvall, Danny Lloyd, Scatman Crothers, Barry Nelson, Philip Stone, Joe Turkel, Anne Jackson, Tony Burton, Lia Beldam",
    "A Nightmare on Elm Street": "Heather Langenkamp, Robert Englund, John Saxon, Ronee Blakley, Amanda Wyss, Jsu Garcia, Johnny Depp, Charles Fleischer, Joseph Whipp",
    "Talk to Me": "Sophie Wilde, Alexandra Jensen, Joe Bird, Otis Dhanji, Miranda Otto, Zoe Terakes, Chris Alosio, Marcus Johnson, Alexandria Steffensen",
    "M3GAN": "Allison Williams, Violet McGraw, Ronny Chieng, Amie Donald, Jenna Davis, Brian Jordan Alvarez, Jen Van Epps, Stephane Garneau-Monten, Lori Dungey",
    "Project Hail Mary": "Ryan Gosling, Sandra Hüller (Upcoming Cast - Project Hail Mary)",
    "Stranger Things": "Winona Ryder, David Harbour, Finn Wolfhard, Millie Bobby Brown, Gaten Matarazzo, Caleb McLaughlin, Natalia Dyer, Charlie Heaton, Cara Buono, Joe Keery, Noah Schnapp, Sadie Sink, Maya Hawke, Priah Ferguson",
    "Shōgun": "Hiroyuki Sanada, Cosmo Jarvis, Anna Sawai, Tadanobu Asano, Takehiro Hira, Tommy Bastow, Fumi Nikaido, Shinnosuke Abe, Tokuma Nishioka",
    "The Boys": "Karl Urban, Jack Quaid, Antony Starr, Erin Moriarty, Dominique McElligott, Jessie T. Usher, Laz Alonso, Chace Crawford, Tomer Capone, Karen Fukuhara, Nathan Mitchell, Colby Minifie, Claudia Doumit, Jensen Ackles",
    "The Office": "Steve Carell, Rainn Wilson, John Krasinski, Jenna Fischer, B.J. Novak, Melora Hardin, David Denman, Leslie David Baker, Brian Baumgartner, Kate Flannery, Angela Kinsey, Oscar Nunez, Phyllis Smith, Ed Helms, Mindy Kaling, Craig Robinson, Ellie Kemper",
    "Friends": "Jennifer Aniston, Courteney Cox, Lisa Kudrow, Matt LeBlanc, Matthew Perry, David Schwimmer, James Michael Tyler, Elliott Gould, Christina Pickles, Maggie Wheeler, Paul Rudd, Jane Sibbett",
    "Wednesday": "Jenna Ortega, Gwendoline Christie, Riki Lindhome, Jamie McShane, Hunter Doohan, Percy Hynes White, Emma Myers, Joy Sunday, Georgie Farmer, Naomi J. Ogawa, Christina Ricci, Catherine Zeta-Jones, Luis Guzmán",
    "The Night Manager": "Tom Hiddleston, Hugh Laurie, Olivia Colman, Tom Hollander, Elizabeth Debicki, Alistair Petrie, Natasha Little, Douglas Hodge, David Harewood, Tobias Menzies",
    "Succession": "Brian Cox, Jeremy Strong, Sarah Snook, Kieran Culkin, Alan Ruck, Matthew Macfadyen, Nicholas Braun, J. Smith-Cameron, Peter Friedman, David Rasche, Fisher Stevens, Alexander Skarsgård",
    "Ted Lasso": "Jason Sudeikis, Hannah Waddingham, Jeremy Swift, Phil Dunster, Brett Goldstein, Brendan Hunt, Nick Mohammed, Juno Temple, Sarah Niles, Anthony Head, Toheeb Jimoh, Cristo Fernández, Kola Bokinni",
    "The Legend of Vox Machina": "Laura Bailey, Taliesin Jaffe, Ashley Johnson, Matthew Mercer, Liam O'Brien, Marisha Ray, Sam Riegel, Travis Willingham",
    "Squid Game": "Lee Jung-jae, Park Hae-soo, Wi Ha-joon, HoYeon Jung, O Yeong-su, Heo Sung-tae, Anupam Tripathi, Kim Joo-ryoung, Yoo Sung-joo, Lee Yoo-mi, Gong Yoo, Lee Byung-hun",
    "From": "Harold Perrineau, Catalina Sandino Moreno, Eion Bailey, David Alpay, Elizabeth Saunders, Shaun Majumder, Scott McCord, Ricky He, Chloe Van Landschoot, Pegah Ghafoori, Corteon Moore, Hannah Cheramy",
    "Dark": "Louis Hofmann, Karoline Eichhorn, Lisa Vicari, Maja Schöne, Stephan Kampwirth, Jördis Triebel, Andreas Pietschmann, Paul Lux, Moritz Jahn, Christian Hutcherson, Oliver Masucci",
    "Alice in the Borderland": "Kento Yamazaki, Tao Tsuchiya, Nijiro Murakami, Yuki Morinaga, Keita Machida, Ayaka Miyoshi, Dori Sakurada, Aya Asahina, Shuntaro Yanagi, Yutaro Watanabe, Ayame Misaki",
    "Moon Knight": "Oscar Isaac, Ethan Hawke, May Calamawy, F. Murray Abraham, Ann Akinjirin, David Ganly, Khalid Abdalla, Gaspard Ulliel, Antonia Salib, Fernanda Andrade",
    "Chernobyl": "Jared Harris, Stellan Skarsgård, Paul Ritter, Jessie Buckley, Adam Nagaitis, Con O'Neill, Adrian Rawlins, Sam Troughton, Robert Pugh, David Dencik, Emily Watson",
    "The Boroughs": "Alfred Molina, Geena Davis, Alfre Woodard, Denis O'Hare, Clarke Peters, Bill Pullman",
    "Spider-Noir": "Nicolas Cage, Lamorne Morris, Brendan Gleeson, Abraham Popoola, Li Jun Li, Jack Huston",
    "Scam 1992": "Pratik Gandhi, Shreya Dhanwanthary, Anjali Barot, Hemant Kher, Chirag Vohra, Brinda Trivedi, Ananth Mahadevan, Satish Kaushik, Rajat Kapoor, Nikhil Dwivedi",
    "The Last of Us": "Pedro Pascal, Bella Ramsey, Gabriel Luna, Anna Torv, Nico Parker, John Hannah, Merle Dandridge, Josh Brener, Christopher Heyerdahl, Murray Bartlett, Nick Offerman, Melanie Lynskey",
    "The Haunting of Hill House": "Michiel Huisman, Carla Gugino, Bruce Greenwood, Elizabeth Reaser, Oliver Jackson-Cohen, Kate Siegel, Victoria Pedretti, Timothy Hutton, Henry Thomas, Annabeth Gish",
    "Farzi": "Shahid Kapoor, Vijay Sethupathi, Kay Kay Menon, Raashii Khanna, Bhuvan Arora, Zakir Hussain, Chittaranjan Giri, Amol Palekar, Regina Cassandra",
    "The Family Man": "Manoj Bajpayee, Samantha Ruth Prabhu, Priyamani, Sharib Hashmi, Shreya Dhanwanthary, Sunny Hinduja, Sharad Kelkar, Dalip Tahil, Seema Biswas, Asif Basra",
    "Asur": "Arshad Warsi, Barun Sobti, Riddhi Dogra, Anupriya Goenka, Amey Wagh, Pawan Chopra, Vishesh Bansal, Gaurav Arora, Meiyang Chang",
    "It": "Bill Skarsgård, Jaeden Martell, Finn Wolfhard, Sophia Lillis, Jeremy Ray Taylor, Chosen Jacobs, Jack Dylan Grazer, Wyatt Oleff, Jackson Robert Scott, Nicholas Hamilton, Jessica Chastain, James McAvoy, Bill Hader, Isaiah Mustafa",
    "Dune": "Timothée Chalamet, Rebecca Ferguson, Oscar Isaac, Jason Momoa, Stellan Skarsgård, Stephen McKinley Henderson, Josh Brolin, Javier Bardem, Sharon Duncan-Brewster, Chang Chen, Dave Bautista, David Dastmalchian, Zendaya, Charlotte Rampling",
    "Avatar": "Sam Worthington, Zoe Saldaña, Sigourney Weaver, Stephen Lang, Kate Winslet, Cliff Curtis, Joel David Moore, CCH Pounder, Edie Falco, Brendan Cowell, Jemaine Clement, Jamie Flatters",
    "Avengers": "Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth, Scarlett Johansson, Jeremy Renner, Tom Hiddleston, Clark Gregg, Cobie Smulders, Stellan Skarsgård, Samuel L. Jackson, Gwyneth Paltrow",
    "The Conjuring": "Vera Farmiga, Patrick Wilson, Ron Livingston, Lili Taylor, Shanley Caswell, Hayley McFarland, Joey King, Mackenzie Foy, Kyla Deaver, Shannon Kook, John Brotherton",
    "Interstellar": "Matthew McConaughey, Anne Hathaway, Jessica Chastain, Bill Irwin, Ellen Burstyn, Michael Caine, John Lithgow, Timothée Chalamet, Mackenzie Foy, David Oyelowo, Wes Bentley, Topher Grace, Casey Affleck, Matt Damon",
    "Gladiator": "Russell Crowe, Joaquin Phoenix, Connie Nielsen, Oliver Reed, Richard Harris, Derek Jacobi, Djimon Hounsou, David Schofield, John Shrapnel, Tomas Arana, Ralf Moeller",
    "Inception": "Leonardo DiCaprio, Ken Watanabe, Joseph Gordon-Levitt, Marion Cotillard, Elliot Page, Tom Hardy, Cillian Murphy, Tom Berenger, Michael Caine, Lukas Haas",
    "Oppenheimer": "Cillian Murphy, Emily Blunt, Matt Damon, Robert Downey Jr., Florence Pugh, Josh Hartnett, Casey Affleck, Rami Malek, Kenneth Branagh, Benny Safdie, Jason Clarke",
    "Mad Max": "Tom Hardy, Charlize Theron, Nicholas Hoult, Hugh Keays-Byrne, Josh Helman, Nathan Jones, Zoë Kravitz, Rosie Huntington-Whiteley, Riley Keough, Abbey Lee",
    "Hereditary": "Toni Collette, Alex Wolff, Milly Shapiro, Ann Dowd, Gabriel Byrne, Mallory Bechtel, Zachary Arthur, Mark O'Brien",
    "The Godfather": "Marlon Brando, Al Pacino, James Caan, Richard S. Castellano, Robert Duvall, Sterling Hayden, John Marley, Richard Conte, Diane Keaton, John Cazale, Talia Shire",
    "A Quiet Place": "Emily Blunt, John Krasinski, Millicent Simmonds, Noah Jupe, Cade Woodward, Leon Russom, Cillian Murphy, Djimon Hounsou, Lupita Nyong'o, Joseph Quinn",
    "The Shawshank Redemption": "Tim Robbins, Morgan Freeman, Bob Gunton, William Sadler, Clancy Brown, Gil Bellows, Mark Rolston, James Whitmore, Jeffrey DeMunn",
    "Parasite": "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong, Choi Woo-shik, Park So-dam, Lee Jung-eun, Jang Hye-jin, Park Myung-hoon, Jung Ji-so, Jung Hyun-jun",
    "Get Out": "Daniel Kaluuya, Allison Williams, Bradley Whitford, Caleb Landry Jones, Stephen Root, Lakeith Stanfield, Catherine Keener, Lil Rel Howery, Betty Gabriel, Marcus Henderson",
    "Blade Runner": "Harrison Ford, Rutger Hauer, Sean Young, Edward James Olmos, M. Emmet Walsh, Daryl Hannah, William Sanderson, Brion James, Joe Turkel, Joanna Cassidy, Ryan Gosling, Ana de Armas",
    "Shutter Island": "Leonardo DiCaprio, Mark Ruffalo, Ben Kingsley, Michelle Williams, Emily Mortimer, Patricia Clarkson, Max von Sydow, Jackie Earle Haley, Ted Levine, John Carroll Lynch",
    "The Hangover": "Bradley Cooper, Ed Helms, Zach Galifianakis, Justin Bartha, Heather Graham, Sasha Barrese, Jeffrey Tambor, Ken Jeong, Rachael Harris, Mike Tyson",
    "Superbad": "Jonah Hill, Michael Cera, Christopher Mintz-Plasse, Bill Hader, Seth Rogen, Emma Stone, Martha MacIsaac, Clark Duke, Joe Lo Truglio, Kevin Corrigan",
    "The Dark Knight": "Christian Bale, Heath Ledger, Aaron Eckhart, Michael Caine, Maggie Gyllenhaal, Gary Oldman, Morgan Freeman, Cillian Murphy, Tom Hardy, Anne Hathaway, Marion Cotillard, Joseph Gordon-Levitt",
    "Batman Begins": "Christian Bale, Michael Caine, Liam Neeson, Katie Holmes, Gary Oldman, Cillian Murphy, Tom Wilkinson, Rutger Hauer, Ken Watanabe, Mark Boone Junior",
    "John Wick": "Keanu Reeves, Michael Nyqvist, Alfie Allen, Adrianne Palicki, Bridget Moynahan, Dean Winters, Ian McShane, John Leguizamo, Willem Dafoe, Laurence Fishburne, Halle Berry, Donnie Yen, Bill Skarsgård",
    "The Matrix": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving, Joe Pantoliano, Marcus Chong, Anthony Ray Parker, Julian Arahanga, Matt Doran, Gloria Foster"
}

def update_casts():
    sys.stdout.reconfigure(encoding='utf-8')
    print("Connected to database:", django.db.connection.settings_dict['NAME'])
    
    movies = Movie.objects.all()
    updated_count = 0
    
    for movie in movies:
        title = movie.title
        best_match = None
        
        # Exact match logic or substring match
        for key, cast_list in extended_casts.items():
            if key.lower() in title.lower() or title.lower() in key.lower():
                # To prevent "Spider-Man" overriding "Spider-Noir"
                if "spider-man" in key.lower() and "noir" in title.lower():
                    continue
                if "the dark knight" in key.lower() and "batman" in title.lower():
                    continue
                best_match = cast_list
                break
                
        if not best_match and movie.parent:
            parent_title = movie.parent.title
            for key, cast_list in extended_casts.items():
                if key.lower() in parent_title.lower() or parent_title.lower() in key.lower():
                    best_match = cast_list
                    break
        
        if best_match:
            movie.cast = best_match
            movie.save(update_fields=['cast'])
            updated_count += 1
            print(f"Updated cast for: {movie.title}")
        else:
            print(f"No cast found for: {movie.title}")
            
    print(f"\nDone! Updated {updated_count} out of {movies.count()} records.")

if __name__ == "__main__":
    update_casts()
