for address in "神奈川県横浜市" "神奈川県川崎市川崎区" "神奈川県川崎市幸区" "神奈川県川崎市中原区" "東京都渋谷区" "東京都大田区"; do
    for specialization in "内科" "小児科"; do
        python main.py --address "$address" --specialization "$specialization"
    done
done