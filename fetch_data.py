{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "295b24dc-84bb-4d68-b125-1988a3fcc9aa",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✅ Loaded 103 wallets\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "100%|████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<?, ?it/s]\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✅ Saved raw data to: C:\\Users\\Suyash\\Desktop\\compound-risk-scoring\\data\\compound_raw_data.json\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Fetching data: 100%|█████████████████████████████████████████████████████████████████| 100/100 [01:08<00:00,  1.47it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✅ Saved transaction data for 0 wallets to C:\\Users\\Suyash\\Desktop\\compound-risk-scoring\\data\\wallet_transactions.json\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\n"
     ]
    }
   ],
   "source": [
    "import os\n",
    "import pandas as pd\n",
    "import requests\n",
    "from tqdm import tqdm\n",
    "\n",
    "base_dir = r\"C:\\Users\\Suyash\\Desktop\\compound-risk-scoring\"\n",
    "wallets_csv = os.path.join(base_dir, \"data\", \"wallets.csv\")\n",
    "\n",
    "wallets_df = pd.read_csv(wallets_csv)\n",
    "wallets_df.columns = [\"wallet_id\"]\n",
    "wallets = wallets_df[\"wallet_id\"].tolist()\n",
    "\n",
    "print(f\"✅ Loaded {len(wallets)} wallets\")\n",
    "\n",
    "all_data = []\n",
    "\n",
    "for wallet in tqdm(wallets[:5]):  \n",
    "\n",
    "    tx_data = {\n",
    "        \"wallet\": wallet,\n",
    "        \"dummy_feature\": 1,\n",
    "        \"tx_count\": 0,\n",
    "    }\n",
    "    all_data.append(tx_data)\n",
    "\n",
    "output_path = os.path.join(base_dir, \"data\", \"compound_raw_data.json\")\n",
    "pd.DataFrame(all_data).to_json(output_path, orient=\"records\", indent=2)\n",
    "\n",
    "print(f\"✅ Saved raw data to: {output_path}\")\n",
    "import requests\n",
    "import time\n",
    "import json\n",
    "\n",
    "COMPOUND_V2_ENDPOINT = \"https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2\"\n",
    "\n",
    "def fetch_transactions(wallet):\n",
    "    query = \"\"\"\n",
    "    {\n",
    "      account(id: \"%s\") {\n",
    "        id\n",
    "        tokens {\n",
    "          symbol\n",
    "          balance\n",
    "        }\n",
    "        borrowEvents {\n",
    "          amount\n",
    "          blockNumber\n",
    "          timestamp\n",
    "          underlyingSymbol\n",
    "        }\n",
    "        supplyEvents {\n",
    "          amount\n",
    "          blockNumber\n",
    "          timestamp\n",
    "          underlyingSymbol\n",
    "        }\n",
    "      }\n",
    "    }\n",
    "    \"\"\" % wallet.lower()\n",
    "\n",
    "    try:\n",
    "        response = requests.post(\n",
    "            COMPOUND_V2_ENDPOINT,\n",
    "            json={\"query\": query}\n",
    "        )\n",
    "        response.raise_for_status()\n",
    "        return response.json()\n",
    "    except Exception as e:\n",
    "        print(f\"❌ Error fetching {wallet[:10]}: {e}\")\n",
    "        return None\n",
    "\n",
    "all_data = {}\n",
    "\n",
    "for wallet in tqdm(wallets[:100], desc=\"Fetching data\"): \n",
    "    result = fetch_transactions(wallet)\n",
    "    if result and \"data\" in result:\n",
    "        all_data[wallet] = result[\"data\"]\n",
    "    time.sleep(0.5) \n",
    "\n",
    "output_path = os.path.join(base_dir, \"data\", \"wallet_transactions.json\")\n",
    "with open(output_path, \"w\") as f:\n",
    "    json.dump(all_data, f)\n",
    "\n",
    "print(f\"✅ Saved transaction data for {len(all_data)} wallets to {output_path}\")\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "cfcdbd13-db7a-43cc-bd3b-5a10a07ff750",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
