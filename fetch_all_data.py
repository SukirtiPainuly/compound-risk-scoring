{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "2cbf9bd7-0251-4968-8b97-1fcd426f63b2",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Fetching wallet transactions: 100%|██████████████████████████████████████████████████| 103/103 [01:13<00:00,  1.41it/s]\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "✅ Done! Saved all transaction data to: C:\\Users\\Suyash\\Desktop\\compound-risk-scoring\\data\\all_wallets_data.json\n"
     ]
    }
   ],
   "source": [
    "import os\n",
    "import json\n",
    "import pandas as pd\n",
    "import requests\n",
    "import time\n",
    "from tqdm import tqdm\n",
    "\n",
    "\n",
    "wallets_df = pd.read_csv(r\"C:\\Users\\Suyash\\Desktop\\compound-risk-scoring\\data\\wallets.csv\")\n",
    "wallets_df.columns = ['wallet_id']\n",
    "wallets = wallets_df['wallet_id'].tolist()\n",
    "\n",
    "MORALIS_API_KEY = \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjUxYTI4NTNlLTUxMGMtNDljMS1hMmY2LTdhZGE0Zjc5OTdjYSIsIm9yZ0lkIjoiNDYxMzYxIiwidXNlcklkIjoiNDc0NjUzIiwidHlwZUlkIjoiMjQ0ZjdjZTktZmFkZS00ODE1LThhNmEtYTg3ZDIzNDk3ZjBhIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3NTM0NTA1NzIsImV4cCI6NDkwOTIxMDU3Mn0.HzOe_UR8z8R3s3dJL9jLAZgsASlipuft7Edci6_pkkk\"  # (Already set)\n",
    "\n",
    "headers = {\n",
    "    \"accept\": \"application/json\",\n",
    "    \"X-API-Key\": MORALIS_API_KEY\n",
    "}\n",
    "\n",
    "all_data = []\n",
    "for wallet in tqdm(wallets, desc=\"Fetching wallet transactions\"):\n",
    "    url = f\"https://deep-index.moralis.io/api/v2.2/{wallet}/erc20/transfers?chain=eth&limit=100\"\n",
    "\n",
    "    try:\n",
    "        response = requests.get(url, headers=headers)\n",
    "        if response.status_code == 200:\n",
    "            wallet_data = response.json()\n",
    "            all_data.append({\"wallet\": wallet, \"transactions\": wallet_data})\n",
    "        else:\n",
    "            print(f\"Failed to fetch {wallet} – Status code:\", response.status_code)\n",
    "    except Exception as e:\n",
    "        print(f\"Error for wallet {wallet}: {e}\")\n",
    "\n",
    "    time.sleep(0.2)  \n",
    "\n",
    "# Save to file\n",
    "output_path = r\"C:\\Users\\Suyash\\Desktop\\compound-risk-scoring\\data\\all_wallets_data.json\"\n",
    "with open(output_path, \"w\") as f:\n",
    "    json.dump(all_data, f, indent=2)\n",
    "\n",
    "print(f\"\\n✅ Done! Saved all transaction data to: {output_path}\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1a98e415-6771-481a-a5c5-522a5996a5a1",
   "metadata": {},
   "outputs": [],
   "source": [
    "|"
   ]
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
