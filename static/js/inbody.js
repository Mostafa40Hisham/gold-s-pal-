function calculateInBody() {
    // Get user inputs
    const weight = parseFloat(document.getElementById('weight').value);
    const height = parseFloat(document.getElementById('height').value);
    const age = parseInt(document.getElementById('age').value);
    const gender = document.getElementById('gender').value;
    const activity = parseFloat(document.getElementById('activity').value);
  
    // Validate inputs
    if (isNaN(weight) || isNaN(height) || isNaN(age)) {
      alert('Please enter valid inputs!');
      return;
    }
  
    // Calculate BMR
    let bmr = gender === 'male' 
      ? 10 * weight + 6.25 * height - 5 * age + 5
      : 10 * weight + 6.25 * height - 5 * age - 161;
  
    // Calculate TDEE
    const tdee = (bmr * activity).toFixed(2);
  
    // Approximate body fat percentage
    const bodyFat = gender === 'male'
      ? (1.2 * (weight / Math.pow(height / 100, 2)) + 0.23 * age - 16.2).toFixed(2)
      : (1.2 * (weight / Math.pow(height / 100, 2)) + 0.23 * age - 5.4).toFixed(2);
  
    // Calculate fat mass and muscle mass
    const fatMass = ((bodyFat / 100) * weight).toFixed(2);
    const muscleMass = (weight - fatMass).toFixed(2);
  
    // Display results
    document.getElementById('results').innerHTML = `
      <p>Daily Calorie Needs: <strong>${tdee} kcal</strong></p>
      <p>Body Fat Percentage: <strong>${bodyFat}%</strong></p>
      <p>Fat Mass: <strong>${fatMass} kg</strong></p>
      <p>Muscle Mass: <strong>${muscleMass} kg</strong></p>
    `;
  }
  