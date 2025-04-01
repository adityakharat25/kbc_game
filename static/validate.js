function validateDOB() {
    let dobInput = document.getElementById("dob").value;
    let dob = new Date(dobInput);
    let today = new Date();

    let age = today.getFullYear() - dob.getFullYear();
    let monthDiff = today.getMonth() - dob.getMonth();
    let dayDiff = today.getDate() - dob.getDate();

    if (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0)) {
        age--; // Adjust age if birthday hasn't occurred yet this year
    }

    if (age < 12 && age > 0) {
        alert("You must be at least 12 years old to register.");
        return false;
    }
    if (age < 0) {
        alert("Date of Birth can't be in the future.");
        return false;
    }
    if (age >= 100) {
        alert("Enter a proper age!");
        return false;
    }

    return true;
}
