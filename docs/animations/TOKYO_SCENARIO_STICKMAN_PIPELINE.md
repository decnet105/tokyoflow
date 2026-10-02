# TokyoFlow: Stickman Animation Pipeline for Situational Japanese
## Explaining Complex Cultural & Linguistic Mechanics via 60-Second Minimalist Animations

---

### 1. Pedagogical Rationale
Japanese daily life is full of **invisible social rules, implicit registers, and rapid-fire conversational scripts**. 
Textbooks explain these with dry, intimidating paragraphs. 
By utilizing the **Stickman Explainer Skill** (`skills/stickman-explainer/`):
- We turn 1 complex Tokyo social mechanism into a **6-scene, 60-second animated micro-story**.
- Uses high-contrast 2D line-art with Tokyo accent colors (JR Green, Tokyo Metro Blue, Kombini Orange).
- Highly shareable on mobile (9:16 vertical video for iOS in-app micro-lessons, TikTok, Instagram Reels, YouTube Shorts).

---

### 2. Standard 6-Scene Stickman Storyboard Template for Tokyo Scenarios

```
+--------------------------------------------------------------------------------------------------+
|                               6-SCENE TOKYO SCENARIO ANIMATION ARC                               |
+-----------+-----------------------------------+--------------------------------------------------+
| Scene #   | Emotional Beat                    | Tokyo Visual Gag / Mechanism                     |
+-----------+-----------------------------------+--------------------------------------------------+
| Scene 1   | The Daily Life Freeze (Hook)      | Stickman freezes in front of Tokyo cashier/gate. |
| Scene 2   | The Hidden Rule / Mechanism       | Diagram shows what the staff is actually asking. |
| Scene 3   | The Mistake / Trap                | What happens if you use Duolingo's literal reply.|
| Scene 4   | The Tokyo Native Shortcut         | 1-line native magic phrase (e.g. "Issho de ii").|
| Scene 5   | The Smooth Resolution             | Staff smiles, nod of mutual unspoken flow.       |
| Scene 6   | Takeaway / Passport Check         | Can-Do badge unlock & flashcard summary.         |
+-----------+-----------------------------------+--------------------------------------------------+
```

---

### 3. Example 1: "The 7-Eleven Cashier Script Decoded" (Convenience Store)

- **Ratio**: `9:16` (Vertical Mobile)
- **Visual Style**: Style 1 (Minimalist Line Art with Pure White Canvas & Kombini Orange Accent)

#### Director's Proposal & Narration

| Scene | Duration | Visual Action | Spoken Narration (JP + EN Subtitles) |
| :--- | :--- | :--- | :--- |
| **01** | 0-10s | Stickman places bento on counter. Cashier fires 5 question speech bubbles in 2 seconds. Stickman sweats. | … *(At Japanese convenience store checkouts, cashiers fire rapid-fire questions... what are they asking?)* |
| **02** | 10-20s | Split-screen checklist popups: 1. Point Card 2. Bento Heating 3. Spoon/Chopsticks 4. Plastic Bag 5. Payment. |  *(It's always the same 5-step script! Point card, microwave, cutlery, bag, payment.)* |
| **03** | 20-30s | Stickman tries to explain in complex textbook Japanese, causing a long queue behind him. |  *(Trying to reply with long textbook sentences holds up the entire rush hour line.)* |
| **04** | 30-40s | Stickman delivers the 3 Tokyo magic shortcuts with glowing checkmarks: (No thanks), (Warm it up), Suica(With Suica). | 3Suica *(You only need 3 magic phrases! "Daijobu desu", "Atatamete kudasai", "Suica de".)* |
| **05** | 40-50s | Cashier hands warm bento with quick bow: . Stickman walks out smoothly. |  *(Checkout complete in 3 seconds! Now you operate like a Tokyo local.)* |
| **06** | 50-60s | Tokyo Residence Passport stamps the "A1 Kombini Checkout" Can-Do badge. | TokyoFlow1 *(Master real Tokyo daily life with TokyoFlow!)* |

---

### 4. Integration into TokyoFlow iOS App
- The generated stickman animations are exported as lightweight H.264 / AVPlayer clips.
- Embedded as 10-second animated intros inside [`ScenarioDetailView.swift`](file:///Users/kilvonwu/Documents/UseCaseDrivenJapanese/TokyoFlow/Views/Scenario/ScenarioDetailView.swift) before starting live interactive roleplays.
- Serves as the primary visual explainer for cultural hacks and manga reading tips.
