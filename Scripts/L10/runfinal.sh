for name in "AgTi" "AlMg" "AlTi" "AuCu" "NiFe" "NiMg" "PdFe" "PdTi" "PtCo" "PtFe" "PtNi" "ZrMg"
do
	openmd $name"L10Final.omd"
	openmd $name"L10ZhouFinal.omd"

	elasticConstants -i $name"L10Final.eor" > $name"D.elastic"
	elasticConstants -i $name"L10ZhouFinal.eor" > $name"Z.elastic"


done
