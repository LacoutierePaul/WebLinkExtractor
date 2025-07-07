awk '
{
  gsub(/^https?:\/\//, "")         # supprimer protocole
  sub(/\.$/, "")                   # supprimer point final
  line=tolower($0)                 # tout mettre en minuscules
  n=split(line, p, ".")
  if(n>=2) print p[n-1]"."p[n]   # garder domaine racine
}	
' domains.txt | sort -u		# trie et supprime les doublons 		
