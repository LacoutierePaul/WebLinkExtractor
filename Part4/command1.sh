sed -E 's|https?://||; s|\.$||' domains.txt | \
awk '
{
  # mettre en minuscules
  line=tolower($0)
  # split par .
  n=split(line, parts, ".")
  # récupérer les 2 derniers labels pour avoir domaine racine
  if (n>=2) {
    print parts[n-1]"."parts[n]
  }
}
' | sort -u # trie et supprimes les doublons
