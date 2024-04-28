# Moosic Unsupervised Machine Learning Project

<p align='center'>
  <img src="images/Logos1b.png">
</p>


## Project Goal

Goal of this project is to support musical experts from a fictional company called *Moosic*.
*Moosic* takes pride in providing manually crafted playlists for music enthusiasts of all genres.
As the start-up company is growing rapidly their experts struggle to keep the pace and create more and more playlists.
So the idea is to employ a machine learning tool to provide them with preselected songs and simplify their way of working.<br>

Being part of a data science bootcamp, the intent of this project was getting started in scikit-learn.<br>
I extended the official goals of the project by also retrieving genre-data using Gemini AI and wrapping everything up in an Online Dashboard-app made with streamlit.


## Results & Summary

You'll find a list of key-points about the outcome of the project in the following.<br>
Please look below for more insights to specific topics.<br>

1. **Dataset**<br>
   A dataset of +5000 songs including their auditive features was provided.

2. **Clustering**<br>
   Using SciKit Learn the songs were grouped into 22 different clusters based on their auditive similarity.
   The KMeans algorithm provided generally favorable results, however some outlying results (e.g. death metal in a mostly pop-music cluster) could not be avoided.

3. **Quality assessement**<br>
   Quality was first assessed by manually listening to samples from the resulting clusters. As this obviously proved to be too time-consuming, genres were assigned automatically to the individual artists.
   This was done using Google Gemini AI.<br>
   Quality was then defined as "purity of genres" per auditive cluster. Although it might not be the most *natural* parameter for QA, it is automatable and thereby preferred when working with a dataset of this size.<br>

4. **Assistant App**<br>
   To make the life of *Moosic*s musical experts easier, an assistant app was created using Streamlit.<br>
   The app provides the cluster-results to the experts, helping them to generate playlists faster and with less effort.<br>
   <br>


**Things to note:**<br>
- Genre-assignment per artist using Gemini AI wasn't 100% accurate, but provided a usable base for quality assessement.
- The average genre of an artist does not necessarily represent the genre of specific song (e.g. an acoustic ballad from an otherwise heavy metal band). Proper labeling should incorporate that.
- After having genre's assigned to the songs it might make more sense to use a supervised ML-approach instead, which wasn't part of the project's scope.


## Streamlit App

The streamlit app provides a user-interface for *Moosic*s musical experts to support their work of playlist-creation.<br>
First, it shows the ML-generated clusters and their top 3 genres. Experts may then select one or multiple clusters as a base for their playist. Songs contained in those clusters are then displayed as a table, also mentioning each artist's genre.<br>
An embedded spotify-player also allows experts to listen to selected songs directly.<br>
<br>
The last part of the app gives the musical experts an understanding of the machine learning process. They can choose an additional song to compare against their previous selection.
Auditive features of those songs are then interactively visualized, as well as numerically listed in a table.<br>
The Visualization especially shows the outcome of the ML-process very well: Combinations of auditive features per song result in various polygon-shapes per cluster.
Looking at different songs from the same cluster shows that their visual-representation is generally similar, even if they might be (incorrectly) from two different genres.<br>
<br>
<br>
*Click one of the images below or <a href="mossic.streamlit.app">[here]</a> to get to the app and try it out yourself!*<br>
<br>

<p align='center'>
  <a href="https://moosic.streamlit.app/">
    <img src="images/Moosic_Embed.png">
  </a>
</p>
<br>

<p align='center'>
  <a href="https://moosic.streamlit.app/">
    <img src="images/Moosic_2.png" width=400>
  </a>
  <a href="https://moosic.streamlit.app/">
    <img src="images/Moosic_3.png" width=400>
  </a>
</p>


## Project presentation

The following shows parts of the project's final presentation to *Moosic*s management.<br>
<br>
*Click <a href="https://docs.google.com/presentation/d/e/2PACX-1vQ2O_4ibPgwQD2fWC6CS441HFvl8W4ctSQ9iAGAm6nHDmJuY71VsRF3sJ6Xbq9CgXxwUSQfh4Pf0HBo/pub?start=true&loop=true&delayms=3000">[here}</a> to get to the full presentation.*<br>
<br>

<p align='center'>
  <img src="images/WBS_Project_03_UnsupML-4.png" width=400> <img src="images/WBS_Project_03_UnsupML-7.png" width=400>
  <br>
  <br>
  <img src="images/WBS_Project_03_UnsupML-10.png" width=400> <img src="images/WBS_Project_03_UnsupML-11.png" width=400>
  <br>
  <br>
  <img src="images/WBS_Project_03_UnsupML-13.png" width=400> <img src="images/WBS_Project_03_UnsupML-14.png" width=400>
  <br>
  <br>
</p>


## Clustering

Song-clustering was done using the kmeans-algorithm with scikit-learn. The available dataset provided a total of 13 different auditive and musical features to parametrize and distinguish the songs.<br>
These features originate from the <a href="https://developer.spotify.com/documentation/web-api">[Spotify Web API]</a>. Since the feature-scaling is not uniform, scaling needs to be applied before passing the songs on to kmeans. For this, sklearn already provides a selection of methods.<br>
For a decision on the number of clusters, <a href="https://www.codecademy.com/learn/dspath-unsupervised/modules/dspath-clustering/cheatsheet">[Inertia]</a> and <a href="https://en.wikipedia.org/wiki/Silhouette_(clustering)">[Silhouette score]</a> were evaluated numerically and visually. Assessing the change-rate of inertia per additional cluster provided a more quantitative way of finding the <a href="https://builtin.com/data-science/elbow-method">[elbow]</a>.
Finally a number of 22 clusters provided accetable values for both of those parameters.<br>
<br>
Dimensionality reduction using principal components analysis (PCA) could have been used for more efficient clustering, but wasn't used due to time constraints and the manageable size of the dataset.
<br>

## Recap & outlook

Clustering using unsupervised machine learning with auditive features generally works okay. The process isn't very complex and clustering happens very fast. In the project's scenario of supporting *Moosic*s musical experts it provides them with a good foundation of generally similar songs to create playlists from. The additionally created streamlit app also works as a handy and simple-to-use device to support the experts.<br>
<br>
As said above, clusters from the ML process still contain some "odd" song choices. They'll probably be easy to spot for the employees, but it's not a 100% ideal result. Evaluating different amounts of clusters might yield more insights into the behaviour of the algorithm on the provided dataset. Also performing "sub-clustering" of primary results could lead to more refined outcomes.<br>
Also Gemini AI's genre-labeling for artists wasn't always fully correct. Having songs and/or artists labeled with a genre makes it obvious to switch from an unsupervised to a supervised ML algorithm.<br>

Generally, a more sophisticated quality assessement including anomaly detection and later on actual user studys *(which were of course not possible in the scope of the bootcamp)* should be employed.<br>
<br>
As an introduction to machine learning the project provided various aspects to explore and generated viable results.<br>
For a more advanded approach, the above mentioned proposals should be implemented.








