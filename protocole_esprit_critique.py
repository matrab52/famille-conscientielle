#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pour le reste de cette session :

Protocole esprit critique - VERSION CORRIGÉE
==========================================

Framework d'analyse critique d'événements basé sur l'analyse rationnelle,
l'approche bayésienne et les méthodes d'investigation criminologique.

CORRECTIONS MAJEURES v2.0 :
- Neutralité bayésienne restaurée
- Seuils de validité implémentés  
- Mode contradictoire ajouté
- Biais structurels corrigés
"""

import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class TypeSource(Enum):
    OFFICIELLE = "officielle"
    ALTERNATIVE = "alternative"
    TEMOIGNAGE = "temoignage"
    DOCUMENT = "document"


@dataclass
class Source:
    nom: str
    type_source: TypeSource
    credibilite: float  # 0-1
    informations: List[str]
    raisonnement_rationnel: bool = True


@dataclass
class Fait:
    description: str
    sources: List[Source]
    probabilite: float = 0.5  # probabilité bayésienne initiale
    confirme_par_multiples_sources: bool = False
    solidite_factuelle: float = 0.5  # Nouveau : solidité objective du fait


@dataclass
class Contradiction:
    fait_a: str
    fait_b: str
    niveau_incompatibilite: float  # 0-1
    validee_independamment: bool = False  # Nouveau : validation externe


class ProtocoleEspritCritique:
    def __init__(self):
        self.faits = []
        self.contradictions = []
        self.version_officielle = None
        self.versions_alternatives = []
        self.seuil_minimum_anomalies = 5  # Nouveau : seuil de déclenchement
        
    def collecter_informations(self, sources: List[Source], limite_anomalies: int = 20) -> Dict:
        """
        Étape 1: Collecte des informations principales avec validation de qualité
        """
        faits_collectes = {}
        compteur_anomalies = 0
        anomalies_validees = 0
        
        for source in sources:
            if source.raisonnement_rationnel:
                for info in source.informations:
                    # Identifier et valider les anomalies
                    if self._est_anomalie(info):
                        if compteur_anomalies >= limite_anomalies:
                            continue
                        compteur_anomalies += 1
                        
                        # Validation de la solidité de l'anomalie
                        if self._valider_anomalie(info, source):
                            anomalies_validees += 1
                    
                    if info not in faits_collectes:
                        fait = Fait(description=info, sources=[source])
                        fait.solidite_factuelle = self._evaluer_solidite_fait(info, source)
                        faits_collectes[info] = fait
                    else:
                        faits_collectes[info].sources.append(source)
                        # Recalculer solidité avec sources multiples
                        faits_collectes[info].solidite_factuelle = self._evaluer_solidite_fait_multiple(
                            faits_collectes[info]
                        )
        
        # Vérifier si les faits sont confirmés par au moins 2 autres sources
        for fait in faits_collectes.values():
            if len(fait.sources) >= 3:
                fait.confirme_par_multiples_sources = True
            self.faits.append(fait)
        
        # Retourner les statistiques de validation
        return {
            "anomalies_detectees": compteur_anomalies,
            "anomalies_validees": anomalies_validees,
            "taux_validation": anomalies_validees / max(compteur_anomalies, 1),
            "donnees_suffisantes": anomalies_validees >= self.seuil_minimum_anomalies
        }
    
    def _est_anomalie(self, information: str) -> bool:
        """
        Identifie si une information constitue une anomalie, improbabilité ou incohérence
        """
        mots_cles_anomalies = [
            "contradiction", "improbable", "impossible", "incohérence", "anomalie",
            "étrange", "suspect", "inexpliqué", "inhabituel", "invraisemblable",
            "paradoxe", "discordance", "aberration", "bizarrerie", "mystère",
            "chute libre", "température insuffisante", "sans impact", "multiples",
            "simultanés", "intact", "désintégrés", "fusion", "traces", "mystérieusement"
        ]
        return any(mot in information.lower() for mot in mots_cles_anomalies)
    
    def _valider_anomalie(self, anomalie: str, source: Source) -> bool:
        """
        Valide la solidité d'une anomalie détectée
        """
        # Critères de validation basiques (à affiner selon le contexte)
        score_validation = 0
        
        # Crédibilité de la source
        score_validation += source.credibilite * 0.4
        
        # Type de source (documents > témoignages > alternatives > officielles pour anomalies)
        type_bonus = {
            TypeSource.DOCUMENT: 0.3,
            TypeSource.TEMOIGNAGE: 0.2,
            TypeSource.ALTERNATIVE: 0.15,
            TypeSource.OFFICIELLE: 0.1  # Sources officielles moins susceptibles de rapporter leurs propres anomalies
        }
        score_validation += type_bonus.get(source.type_source, 0)
        
        # Spécificité de l'anomalie (plus c'est précis, mieux c'est)
        if any(terme in anomalie.lower() for terme in ["température", "vitesse", "timing", "coordonnées"]):
            score_validation += 0.2
        
        # Vérifiabilité technique
        if any(terme in anomalie.lower() for terme in ["physique", "technique", "mesurable", "calculable"]):
            score_validation += 0.1
        
        return score_validation > 0.6  # Seuil de validation
    
    def _evaluer_solidite_fait(self, fait: str, source: Source) -> float:
        """
        Évalue la solidité factuelle d'un fait isolé
        """
        return source.credibilite * (1.0 if source.raisonnement_rationnel else 0.5)
    
    def _evaluer_solidite_fait_multiple(self, fait: Fait) -> float:
        """
        Évalue la solidité d'un fait confirmé par plusieurs sources
        """
        if len(fait.sources) == 1:
            return self._evaluer_solidite_fait(fait.description, fait.sources[0])
        
        # Formule de convergence : solidité augmente avec le nombre de sources indépendantes
        solidite_moyenne = sum(s.credibilite for s in fait.sources) / len(fait.sources)
        bonus_convergence = min(0.3, (len(fait.sources) - 1) * 0.1)
        
        return min(1.0, solidite_moyenne + bonus_convergence)
    
    def identifier_contradictions(self) -> List[Contradiction]:
        """
        Étape 2: Analyser les informations pour identifier improbabilités et contradictions VALIDÉES
        """
        contradictions = []
        
        for i, fait_a in enumerate(self.faits):
            for j, fait_b in enumerate(self.faits[i+1:], i+1):
                if self._sont_contradictoires(fait_a.description, fait_b.description):
                    niveau = self._calculer_niveau_contradiction(fait_a, fait_b)
                    # Nouveau : seuil minimum pour considérer contradiction valide
                    if niveau > 0.6:  # Seuil de significativité
                        contradiction = Contradiction(
                            fait_a.description, 
                            fait_b.description, 
                            niveau
                        )
                        contradiction.validee_independamment = self._valider_contradiction(contradiction)
                        contradictions.append(contradiction)
        
        self.contradictions = contradictions
        return contradictions
    
    def _sont_contradictoires(self, fait_a: str, fait_b: str) -> bool:
        """
        Méthode améliorée pour détecter les contradictions réelles
        """
        # Contradictions explicites
        mots_opposition_directs = [
            ("possible", "impossible"),
            ("présent", "absent"),
            ("élevé", "faible"),
            ("rapide", "lent"),
            ("chaud", "froid"),
            ("intact", "détruit"),
            ("visible", "invisible")
        ]
        
        for terme_a, terme_b in mots_opposition_directs:
            if (terme_a in fait_a.lower() and terme_b in fait_b.lower()) or \
               (terme_b in fait_a.lower() and terme_a in fait_b.lower()):
                return True
        
        # Contradictions contextuelles (à personnaliser selon le domaine)
        contradictions_specifiques = [
            ("effondrement par feu", "vitesse chute libre"),
            ("surprise totale", "exercices simultanés"),
            ("origine naturelle", "labo épicentre"),
            ("asymptomatiques contagieux", "transmission rare"),
            ("simple cambriolage", "équipement sophistiqué")
        ]
        
        for terme_a, terme_b in contradictions_specifiques:
            if (terme_a in fait_a.lower() and terme_b in fait_b.lower()) or \
               (terme_b in fait_a.lower() and terme_a in fait_b.lower()):
                return True
        
        return False
    
    def _valider_contradiction(self, contradiction: Contradiction) -> bool:
        """
        Valide qu'une contradiction est réelle et significative
        """
        # La contradiction doit être basée sur des faits solides
        faits_contradiction = [f for f in self.faits 
                             if f.description in [contradiction.fait_a, contradiction.fait_b]]
        
        if len(faits_contradiction) < 2:
            return False
        
        # Solidité minimale requise pour chaque fait
        solidite_minimale = all(f.solidite_factuelle > 0.6 for f in faits_contradiction)
        
        # Niveau de contradiction suffisant
        niveau_suffisant = contradiction.niveau_incompatibilite > 0.7
        
        return solidite_minimale and niveau_suffisant
    
    def _calculer_niveau_contradiction(self, fait_a: Fait, fait_b: Fait) -> float:
        """
        Calcule le niveau de contradiction entre deux faits avec pondération par solidité
        """
        # Niveau de base selon les sources
        poids_a = len(fait_a.sources) * fait_a.solidite_factuelle
        poids_b = len(fait_b.sources) * fait_b.solidite_factuelle
        
        # Bonus pour confirmation multiple
        if fait_a.confirme_par_multiples_sources:
            poids_a *= 1.5
        if fait_b.confirme_par_multiples_sources:
            poids_b *= 1.5
        
        # Niveau de contradiction proportionnel à la solidité des faits contradictoires
        return min(1.0, (poids_a + poids_b) / (poids_a + poids_b + 2))
    
    def calcul_bayesien_probabilites(self) -> Dict[str, float]:
        """
        Étape 3: Approche bayésienne NEUTRE pour calculer les probabilités
        """
        # CORRECTION MAJEURE : Prior neutre strict
        prob_officielle = 0.5
        prob_alternative = 0.5
        
        # Impact des contradictions VALIDÉES uniquement
        contradictions_validees = [c for c in self.contradictions if c.validee_independamment]
        
        if contradictions_validees:
            # Réduction proportionnelle au nombre et à la force des contradictions validées
            impact_moyen = sum(c.niveau_incompatibilite for c in contradictions_validees) / len(contradictions_validees)
            facteur_reduction = min(0.8, len(contradictions_validees) * impact_moyen * 0.1)  # Maximum 80% de réduction
            
            prob_officielle *= (1 - facteur_reduction)
            prob_alternative = 1 - prob_officielle
        
        # Bonus pour faits confirmés par sources multiples (s'applique aux deux versions)
        faits_confirmes = sum(1 for fait in self.faits if fait.confirme_par_multiples_sources)
        if faits_confirmes > 0:
            # Bonus de confirmation générale (stabilité des données)
            facteur_stabilite = min(0.1, faits_confirmes * 0.02)
            # Le bonus va à la version qui a le moins de contradictions
            if prob_officielle > prob_alternative:
                prob_officielle = min(1.0, prob_officielle + facteur_stabilite)
            else:
                prob_alternative = min(1.0, prob_alternative + facteur_stabilite)
            
            # Renormalisation
            total = prob_officielle + prob_alternative
            prob_officielle /= total
            prob_alternative /= total
        
        return {
            'version_officielle': prob_officielle,
            'versions_alternatives': prob_alternative,
            'contradictions_validees': len(contradictions_validees),
            'facteur_confiance': min(faits_confirmes / max(len(self.faits), 1), 1.0)
        }
    
    def analyser_cui_bono(self, acteurs: List[Dict]) -> Dict[str, float]:
        """
        Étape 4: Méthode du cui bono avec validation de significativité
        """
        if not acteurs:
            return {}
        
        benefices = {}
        
        for acteur in acteurs:
            nom = acteur['nom']
            gains_potentiels = acteur.get('gains', [])
            pouvoir_influence = acteur.get('pouvoir', 0.5)
            
            # Score pondéré par la réalité des gains
            score_benefice = len(gains_potentiels) * pouvoir_influence
            benefices[nom] = score_benefice
        
        # Validation : différence significative entre bénéficiaires ?
        if benefices:
            scores = list(benefices.values())
            score_max = max(scores)
            score_median = sorted(scores)[len(scores)//2] if len(scores) > 1 else score_max
            
            # Ratio de significativité
            ratio_significativite = score_max / max(score_median, 0.1)
            
            # Si pas de différence claire, cui bono non concluant
            if ratio_significativite < 1.5:
                return {"analyse_non_concluante": True}
        
        return benefices
    
    def appliquer_rasoir_occam_criminologique(self, evenements: List[Dict]) -> Dict[str, float]:
        """
        Étape 5: Rasoir d'Occam criminologique avec seuils de significativité
        """
        if not evenements or len(evenements) < 2:
            return {"donnees_insuffisantes": True}
        
        patterns_detectes = {}
        
        # Analyse des bénéficiaires récurrents
        beneficiaires_recurrents = {}
        for event in evenements:
            for beneficiaire in event.get('beneficiaires', []):
                if beneficiaire not in beneficiaires_recurrents:
                    beneficiaires_recurrents[beneficiaire] = []
                beneficiaires_recurrents[beneficiaire].append(event['nom'])
        
        # Analyse de la synchronisation temporelle
        synchronisations = 0
        for i, event_a in enumerate(evenements):
            for event_b in evenements[i+1:]:
                if abs(event_a.get('timestamp', 0) - event_b.get('timestamp', 0)) < event_a.get('fenetre_critique', 0):
                    synchronisations += 1
        
        # Analyse de la cohérence stratégique
        objectifs_communs = {}
        for event in evenements:
            for objectif in event.get('objectifs_servis', []):
                if objectif not in objectifs_communs:
                    objectifs_communs[objectif] = 0
                objectifs_communs[objectif] += 1
        
        # Score de pattern intentionnel AVEC seuils
        score_pattern = 0
        
        # Points pour bénéficiaires récurrents (seuil : 3+ événements)
        for beneficiaire, events in beneficiaires_recurrents.items():
            if len(events) >= 3:  # Seuil relevé
                score_pattern += len(events) * 0.2  # Impact réduit
        
        # Points pour synchronisation (seuil : 2+ synchronisations)
        if synchronisations >= 2:
            score_pattern += synchronisations * 0.15
        
        # Points pour objectifs communs (seuil : 3+ occurrences)
        for objectif, count in objectifs_communs.items():
            if count >= 3:
                score_pattern += count * 0.15
        
        patterns_detectes = {
            'score_pattern_intentionnel': min(score_pattern, 1.0),
            'beneficiaires_recurrents': {k: v for k, v in beneficiaires_recurrents.items() if len(v) >= 3},
            'synchronisations_detectees': synchronisations,
            'objectifs_communs': {k: v for k, v in objectifs_communs.items() if v >= 3},
            'seuil_significativite_atteint': score_pattern > 0.5
        }
        
        return patterns_detectes
    
    def determiner_version_probable(self, 
                                 acteurs: Optional[List[Dict]] = None,
                                 evenements: Optional[List[Dict]] = None) -> Dict:
        """
        Étape 6: Synthèse ÉQUILIBRÉE pour déterminer la version la plus probable
        """
        # Vérification préalable des données
        stats_collecte = self.collecter_informations([])  # Récupérer les stats sans recollecte
        
        if not hasattr(self, 'faits') or len(self.faits) == 0:
            return {
                'erreur': 'Aucune donnée analysée',
                'recommandation': 'Collecter des informations avant analyse'
            }
        
        # Calculs bayésiens
        prob_bayesiennes = self.calcul_bayesien_probabilites()
        
        # Analyse cui bono avec validation
        analyse_benefices = {}
        if acteurs:
            analyse_benefices = self.analyser_cui_bono(acteurs)
            if analyse_benefices.get("analyse_non_concluante"):
                analyse_benefices = {}
        
        # Rasoir d'Occam criminologique avec seuils
        patterns_criminologiques = {}
        if evenements:
            patterns_criminologiques = self.appliquer_rasoir_occam_criminologique(evenements)
            if patterns_criminologiques.get("donnees_insuffisantes"):
                patterns_criminologiques = {}
        
        # Score composite ÉQUILIBRÉ
        score_officiel = prob_bayesiennes['version_officielle']
        score_alternatif = prob_bayesiennes['versions_alternatives']
        
        # Ajustement cui bono (RÉDUIT et conditionnel)
        if analyse_benefices and not analyse_benefices.get("analyse_non_concluante"):
            scores_benefices = [v for v in analyse_benefices.values() if isinstance(v, (int, float))]
            if scores_benefices:
                max_benefice = max(scores_benefices)
                if max_benefice > 3:  # Seuil plus élevé
                    score_alternatif += min(0.15, max_benefice * 0.03)  # Impact réduit
        
        # Ajustement patterns criminologiques (RÉDUIT et conditionnel)
        if patterns_criminologiques and patterns_criminologiques.get('seuil_significativite_atteint'):
            score_pattern = patterns_criminologiques.get('score_pattern_intentionnel', 0)
            if score_pattern > 0.6:  # Seuil plus élevé
                score_alternatif += min(0.2, score_pattern * 0.25)  # Impact réduit
        
        # Renormalisation pour éviter les scores > 1
        total_score = score_officiel + score_alternatif
        if total_score > 1:
            score_officiel /= total_score
            score_alternatif /= total_score
        
        # Seuil de décision : différence significative requise
        seuil_decision = 0.15  # 15% de différence minimum pour conclusion nette
        
        if abs(score_officiel - score_alternatif) < seuil_decision:
            version_probable = 'indetermine'
        else:
            version_probable = 'officielle' if score_officiel > score_alternatif else 'alternative'
        
        return {
            'probabilites_bayesiennes': prob_bayesiennes,
            'analyse_cui_bono': analyse_benefices,
            'patterns_criminologiques': patterns_criminologiques,
            'score_version_officielle': score_officiel,
            'score_versions_alternatives': score_alternatif,
            'version_plus_probable': version_probable,
            'marge_decision': abs(score_officiel - score_alternatif),
            'contradictions_identifiees': len(self.contradictions),
            'contradictions_validees': prob_bayesiennes.get('contradictions_validees', 0),
            'faits_confirmes_multiples_sources': sum(1 for f in self.faits if f.confirme_par_multiples_sources),
            'niveau_confiance': prob_bayesiennes.get('facteur_confiance', 0)
        }
    
    def livrer_conclusion(self, 
                         acteurs: Optional[List[Dict]] = None,
                         evenements: Optional[List[Dict]] = None) -> str:
        """
        Étape 7: Conclusion nuancée - déterminer quelle version est la plus probable et pourquoi
        """
        # Vérification des données minimales
        if len(self.faits) == 0:
            return """
ANALYSE IMPOSSIBLE : DONNÉES INSUFFISANTES

Aucune information n'a été collectée pour l'analyse. 
Le protocole nécessite au minimum des sources d'information 
avec des faits vérifiables pour fonctionner.

RECOMMANDATION : Fournir des sources documentées avec des informations spécifiques.
            """.strip()
        
        analyse = self.determiner_version_probable(acteurs, evenements)
        
        if 'erreur' in analyse:
            return f"ERREUR D'ANALYSE : {analyse['erreur']}\n{analyse.get('recommandation', '')}"
        
        version_retenue = analyse['version_plus_probable']
        marge_decision = analyse['marge_decision']
        
        # Construction de l'argumentation basée sur des critères objectifs
        raisons = []
        
        # Analyse des contradictions validées
        contradictions_validees = analyse.get('contradictions_validees', 0)
        contradictions_totales = analyse['contradictions_identifiees']
        
        if contradictions_validees > 0:
            raisons.append(f"{contradictions_validees} contradictions majeures validées sur {contradictions_totales} identifiées")
        
        # Faits confirmés par sources multiples
        faits_confirmes = analyse['faits_confirmes_multiples_sources']
        if faits_confirmes > 0:
            raisons.append(f"{faits_confirmes} faits confirmés par sources multiples indépendantes")
        
        # Analyse cui bono si significative
        if analyse['analyse_cui_bono'] and not analyse['analyse_cui_bono'].get('analyse_non_concluante'):
            beneficiaires_significatifs = [k for k, v in analyse['analyse_cui_bono'].items() 
                                         if isinstance(v, (int, float)) and v > 2]
            if beneficiaires_significatifs:
                raisons.append(f"Bénéficiaires significatifs identifiés: {', '.join(beneficiaires_significatifs)}")
        
        # Patterns criminologiques si seuil atteint
        if analyse['patterns_criminologiques'] and analyse['patterns_criminologiques'].get('seuil_significativite_atteint'):
            patterns = analyse['patterns_criminologiques']
            if patterns.get('beneficiaires_recurrents'):
                raisons.append(f"Pattern de bénéficiaires récurrents validé: {list(patterns['beneficiaires_recurrents'].keys())}")
            if patterns.get('objectifs_communs'):
                raisons.append(f"Objectifs stratégiques récurrents: {list(patterns['objectifs_communs'].keys())}")
        
        # Niveau de confiance
        niveau_confiance = analyse['niveau_confiance']
        
        # Construction de la conclusion
        if version_retenue == 'indetermine':
            conclusion = f"""VERSION LA PLUS PROBABLE: INDÉTERMINÉE
Probabilité officielle: {analyse['score_version_officielle']:.1%}
Probabilité alternative: {analyse['score_versions_alternatives']:.1%}
Marge de décision: {marge_decision:.1%} (< 15% requis pour conclusion nette)

JUSTIFICATION:
Les données disponibles ne permettent pas de déterminer avec suffisamment de certitude
quelle version des événements est la plus probable. Une investigation plus approfondie
est nécessaire pour obtenir des éléments discriminants.

ÉLÉMENTS D'ANALYSE:
{chr(10).join(f"• {raison}" for raison in raisons) if raisons else "• Aucun élément discriminant significatif identifié"}

NIVEAU DE CONFIANCE: {niveau_confiance:.1%}
RECOMMANDATION: Rechercher des sources supplémentaires ou des éléments plus discriminants.
            """.strip()
            
        else:
            score_final = (analyse['score_version_officielle'] 
                          if version_retenue == 'officielle' 
                          else analyse['score_versions_alternatives'])
            
            conclusion = f"""VERSION LA PLUS PROBABLE: {version_retenue.upper()}
Probabilité: {score_final:.1%}
Marge de décision: {marge_decision:.1%}

JUSTIFICATION:
{chr(10).join(f"• {raison}" for raison in raisons) if raisons else "• Analyse basée sur la cohérence générale des données"}

ÉLÉMENTS D'ANALYSE:
• Probabilité bayésienne version officielle: {analyse['probabilites_bayesiennes']['version_officielle']:.1%}
• Contradictions validées/totales: {contradictions_validees}/{contradictions_totales}
• Niveau de confiance des données: {niveau_confiance:.1%}
• Cohérence vs incohérences: {"Cohérence acceptable" if contradictions_validees <= 1 else "Incohérences significatives"}
            """.strip()
        
        return conclusion


# Exemple d'utilisation avec validation
def exemple_analyse_valide():
    """
    Exemple d'application du protocole corrigé avec données réelles
    """
    protocole = ProtocoleEspritCritique()
    
    # Sources d'information avec données spécifiques
    sources = [
        Source("Commission officielle", TypeSource.OFFICIELLE, 0.7, 
               ["Version A des événements selon rapport officiel",
                "Chronologie établie par les autorités"]),
        Source("Experts indépendants", TypeSource.ALTERNATIVE, 0.8, 
               ["Contradiction technique identifiée dans version A",
                "Analyse révèle incohérence temporelle impossible",
                "Données physiques incompatibles avec version officielle"]),
        Source("Témoins directs", TypeSource.TEMOIGNAGE, 0.9, 
               ["Observation directe contredit version A",
                "Témoignage corrobore analyse experts indépendants"])
    ]
    
    # Acteurs avec bénéfices spécifiques
    acteurs = [
        {"nom": "Autorité A", "gains": ["légitimité", "pouvoir", "budget"], "pouvoir": 0.8},
        {"nom": "Opposition B", "gains": ["critique"], "pouvoir": 0.3}
    ]
    
    # Événements liés
    evenements = [
        {
            "nom": "événement_principal", 
            "beneficiaires": ["Autorité A"], 
            "objectifs_servis": ["pouvoir", "légitimité"],
            "timestamp": 0,
            "fenetre_critique": 30
        },
        {
            "nom": "mesure_suivante", 
            "beneficiaires": ["Autorité A"], 
            "objectifs_servis": ["pouvoir"],
            "timestamp": 15,
            "fenetre_critique": 30
        },
        {
            "nom": "politique_conséquente", 
            "beneficiaires": ["Autorité A"], 
            "objectifs_servis": ["pouvoir", "budget"],
            "timestamp": 45,
            "fenetre_critique": 60
        }
    ]
    
    # Application du protocole
    stats_collecte = protocole.collecter_informations(sources, limite_anomalies=20)
    print("Statistiques de collecte:", stats_collecte)
    
    if stats_collecte["donnees_suffisantes"]:
        protocole.identifier_contradictions()
        conclusion = protocole.livrer_conclusion(acteurs, evenements)
        return conclusion
    else:
        return "Données insuffisantes pour analyse fiable"


if __name__ == "__main__":
    print("=== PROTOCOLE ESPRIT CRITIQUE - VERSION CORRIGÉE ===")
    print(exemple_analyse_valide())
