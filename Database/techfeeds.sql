create table techfeeds(feed_no integer primary key , feed_links char(120), tags char(50),Title varchar(150),summary varchar(500));

insert into techfeeds values (1,"https://www.fedscoop.com/watson-cloud/","IBM Watson","The cognitive cloud? IBM rolls out Watson-as-a-service","Scott Spangler, principal data scientist for IBM Watson Innovations, demonstrates how IBM Watson cognitive technology can now visually display connections in scientific literature and drug information. In this image, Watson displays protein pathways that can help researchers accelerate scientific breakthroughs by spotting linkages that were previously undetected.");

insert into techfeeds values (2,"https://www.forbes.com/sites/roysmythe/2014/09/22/delivering-health-care-by-drone/#4036112b4917","Technology served Mankind","Delivering Health Care By Drone","Could the use of technologies that distance health care providers from the first-hand experience of the suffering of those they care for (such as telemedicine platforms and other forms of “virtual visits” or self-care tools) lead to a collective “stumbling over lines” with unfortunate consequences?");

insert into techfeeds values (3,"https://www.smartdatacollective.com/demise-data-scientist-heresy-or-fact/","Data Science","The Demise of the Data Scientist: Heresy or Fact?"," the data scientist focuses their efforts on developing analytics solutions that solve a specific and unique  business problem");

insert into techfeeds values (4,"https://www.newscientist.com/article/2187599-deepminds-go-playing-software-can-now-beat-you-at-two-more-games/","Deep Learning","DeepMind’s Go playing software can now beat you at two more games","DeepMind’s AI Go master has taught itself new tricks. The latest version of the machine learning software, dubbed AlphaZero, can now also beat the world’s best at chess and shogi – a Japanese game that is similar to chess but played on a bigger board with more pieces.");

insert into techfeeds values (5,"https://www.newscientist.com/article/2186512-exclusive-uk-police-wants-ai-to-stop-violent-crime-before-it-happens/","Artificial Intelligence","UK police wants AI to stop violent crime before it happens","The system, called the National Data Analytics Solution (NDAS), uses a combination of AI and statistics to try to assess the risk of someone committing or becoming a victim of gun or knife crime, as well as the likelihood of someone falling victim to modern slavery.");

insert into techfeeds values (6,"https://www.analyticsindiamag.com/how-qualcomm-investment-in-5-indian-deep-tech-startups-is-paying-off/","Tech World Updates","How Qualcomm’s Investment In 5 Indian Deep Tech Startups Is Paying Off","Qualcomm Ventures recently set up their AI fund to invest up to $100 million in startups which transform artificial intelligence. The fund will focus on startups which want to invest in the area of on-device AI and make the technology more widespread.");

insert into techfeeds values (7,"https://www.analyticsindiamag.com/emergence-of-citizen-data-scientists/","Data Science","Emergence of Citizen Data Scientists","A CDS is different from a true Data Scientist in one crucial way; namely, they do not have the skills or training to be an analyst or a programmer but, with the right tools, they are capable of generating reports, analysing data and sharing data to make decisions.");

insert into techfeeds values (8,"https://www.analyticsindiamag.com/5-paradoxes-which-left-ai-researchers-in-a-lurch/","Artificial Intelligence","5 paradoxes which left AI researchers in a lurch"," The mind concocts and contradicts a million thoughts while using up its residual reasoning to come up with something which betrays its own origin — a paradox.Here is a list of paradoxes that have troubled great minds while in pursuit of making machines more intelligent");

insert into techfeeds values (9,"https://www.analyticsindiamag.com/5-programming-languages-in-fintech-thatll-earn-you-the-fattest-paycheck/","Money for Knowledge","5 Programming Languages In Fintech That’ll Earn You The Fattest Paycheck"," IT professionals with deep knowledge of programming languages are in high demand. In India, we have 5 million developers who still rely heavily on Java, C++ and Python. Besides these popular programming languages, there are other functional languages which can earn developers huge pay cheques.");

insert into techfeeds values (10,"https://www.analyticsindiamag.com/samsung-fakes-portrait-mode-uses-dslr-clicked-photo-as-camera-sample/","Tech World Updates","Samsung Fakes The Portrait Mode; Uses DSLR-Clicked Photo As Its Camera Sample","Mobile phones have started faking demo pictures. Several reports show that mobile companies have been using edited and DSLR-shot photos as their own. This has become a new trend for quite a few mobile phone brands");

select * from techfeeds;
drop table techfeeds;







