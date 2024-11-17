from streamlit_data import streamlit_data
import streamlit as st
import plotly.graph_objects as go


class streamlit_interface:

    def __init__(self):
        self.S = streamlit_data()
        self.show_interface()

    def show_interface(self):
        joueurs = self.S.getAllPlayers()
        categories = ['Points', 'Rebonds', 'Passes']

        joueur = st.selectbox("Choisis un joueur", joueurs, index=0, key='joueur_selectbox')
        categorie = st.selectbox("Choisis une categorie", categories, index=0, key='categorie_selectbox')

        if joueur and categorie:
            cuts = self.S.getAllCuts(joueur, categorie)
            cut = st.selectbox('Choisi un cut', cuts, index=0, key='cut_selectbox')

            if cut is not None and self.S.getAllOddsStats(joueur, categorie, cut) is not None:
                Dates, Cotes, Stats, Cal_Cote = self.S.getAllOddsStats(joueur, categorie, cut)
                self.update_interface(Dates, Cotes, Stats, Cal_Cote, joueur, cut, categorie)

    def update_interface(self, Dates, Cotes, Stats, Cal_Cote, joueur, cut, categorie):
        # Créer une figure Plotly
        fig1 = go.Figure()  # Premier graphique (Cotes et Cal_Cote)
        fig2 = go.Figure()  # Deuxième graphique (Stats)

        # Premier graphique (Cotes et Cal_Cote)
        fig2.add_trace(go.Scatter(
            x=Dates,  # Dates en abscisse
            y=Cotes,  # Cotes en ordonnée
            mode='lines+markers+text',  # Affichage des lignes, des marqueurs et des valeurs sur chaque point
            name='Cotes Winamax',
            text=Cotes,  # Affichage des valeurs des Cotes sur les points
            textposition='top center'  # Position du texte au-dessus des points
        ))

        fig2.add_trace(go.Scatter(
            x=Dates,  # Dates en abscisse
            y=Cal_Cote,  # Cal_Cote en ordonnée
            mode='lines+markers+text',
            name='Cotes Calculés',
            text=Cal_Cote,  # Affichage des valeurs de Cal_Cote sur les points
            textposition='top center'
        ))

        # Deuxième graphique (Stats)
        fig1.add_trace(go.Scatter(
            x=Dates,  # Dates en abscisse
            y=Stats,  # Stats en ordonnée
            mode='lines+markers+text',
            name='Stats',
            text=Stats,  # Affichage des valeurs de Stats sur les points
            textposition='top center'
        ))

        # Configuration de l'axe des ordonnées pour le premier graphique (autoscale)
        fig1.update_layout(
            title=f"Graphique Des Stats de {joueur}",
            xaxis_title="Dates",
            yaxis_title="Valeur",
            yaxis=dict(
                autorange=True,  # Autoscaling de l'axe y
                showgrid=True  # Afficher la grille pour l'axe y
            ),
            legend_title="Listes"
        )


        # Configuration de l'axe des ordonnées pour le deuxième graphique
        fig2.update_layout(
            title=f"Graphique de comparaison des cotes pour : {joueur} a un total de plus de {cut} {categorie}",
            xaxis_title="Dates",
            yaxis_title="Valeur",
            yaxis=dict(
                autorange=True,  # Autoscaling de l'axe y
                showgrid=True
            ),
            legend_title="Listes"
        )
        st.title("SMEXINHO")

        # Affichage des deux graphiques côte à côte
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)

#St = streamlit_interface()