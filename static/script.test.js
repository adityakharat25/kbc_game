const { strToint, resetGame, updatePrizeHighlight } = require('./script'); // Adjust path if needed

// Test for strToint function
describe("strToint function", () => {
    test("should convert comma-separated string to number", () => {
        expect(strToint("1,000")).toBe(1000);
    });

    test("should convert number string without commas", () => {
        expect(strToint("1000000")).toBe(1000000);
    });

    test("should return NaN for empty string", () => {
        expect(strToint("")).toBeNaN();
    });
});

// Mocking DOM elements for game functions
document.body.innerHTML = `
    <div id="prizes">
        <div class="prize">₹1,000</div>
        <div class="prize">₹10,000</div>
        <div class="prize">₹1,00,000</div>
    </div>
    <div id="questionContainer"></div>
`;

describe("updatePrizeHighlight function", () => {
    test("should highlight the correct prize", () => {
        updatePrizeHighlight(1);
        const prizeElements = document.querySelectorAll(".prize");
        expect(prizeElements[1].classList.contains("active")).toBe(true);
    });
});

describe("resetGame function", () => {
    test("should reset game variables", () => {
        resetGame();
        expect(questionIndex).toBe(0);
        expect(selectedOption).toBeNull();
        expect(timeLeft).toBe(45);
    });
});
