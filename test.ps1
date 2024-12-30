# Settings
$ADDRESS = "http://localhost:8000"  # Address of your FastAPI server
$LOGIN = "dan"                      # Username for testing
$PASSWORD = "secretsecret"           # Password for testing
$NEW_PASSWORD = "newsecret"          # New password for update

# Function for sending request and handling errors
function Invoke-ApiRequest {
    param (
        [string]$Uri,
        [string]$Method = "GET",
        [hashtable]$Headers = @{},
        [object]$Body = $null,
        [string]$ContentType = "application/json"
    )

    try {
        $Params = @{
            Uri         = $Uri
            Method      = $Method
            Headers     = $Headers
        }
        if ($Body) {
            $Params.Body = ConvertTo-Json $Body
            $Params.ContentType = $ContentType
        }


        $response = Invoke-RestMethod @Params
        Write-Host "Response from $($Uri): $($response | ConvertTo-Json -Depth 10)"
        return $response
    } catch {
        Write-Host "Error during API request to $($Uri): $_" -ForegroundColor Red
        return $null
    }
}
# Create user (if not exists)
Write-Host "Creating user..."
$createUserResponse = Invoke-ApiRequest -Uri "$ADDRESS/add-user" -Method POST -Body @{"username" = "$LOGIN"; "password" = "$PASSWORD"}
if (!$createUserResponse) {
    Write-Host "Failed to create user. Aborting test." -ForegroundColor Red
    return
}
Write-Host ""
# Get JWT token
Write-Host "Logging in to get JWT token..."
$loginResponse = Invoke-ApiRequest -Uri "$ADDRESS/login" -Method POST -Body @{"username" = "$LOGIN"; "password" = "$PASSWORD"} -ContentType "application/json"
if (!$loginResponse -or !$loginResponse.token) {
    Write-Host "Failed to get JWT token. Aborting test." -ForegroundColor Red
    return
}
$JWT = $loginResponse.token
Write-Host "JWT Token: $($JWT)"
Write-Host ""
# Validate JWT token
Write-Host "Validating JWT token..."
$validateTokenResponse = Invoke-ApiRequest -Uri "$ADDRESS/validate-token" -Method GET -Headers @{"Authorization" = "Bearer $($JWT)"}
if (!$validateTokenResponse -or $validateTokenResponse.message -notlike "Token is valid for user*") {
    Write-Host "JWT is not valid. Aborting test." -ForegroundColor Red
    return
}
Write-Host ""
# Add product
Write-Host "Adding product..."
$addProductResponse = Invoke-ApiRequest -Uri "$ADDRESS/add-product" -Method POST -Headers @{"Authorization" = "Bearer $($JWT)"} -Body @{"name" = "apple"; "price" = 20} -ContentType "application/json"
if (!$addProductResponse) {
    Write-Host "Failed to add product. Aborting test." -ForegroundColor Red
    return
}
Write-Host ""
# Remove product
Write-Host "Removing product..."
$removeProductResponse = Invoke-ApiRequest -Uri "$ADDRESS/remove-from-product" -Method POST -Headers @{"Authorization" = "Bearer $($JWT)"} -Body @{"name" = "apple"; "price" = 20} -ContentType "application/json"
if (!$removeProductResponse) {
    Write-Host "Failed to remove product. Aborting test." -ForegroundColor Red
     return
}
Write-Host ""
# Add product
Write-Host "Adding product..."
$addProductResponse = Invoke-ApiRequest -Uri "$ADDRESS/add-product" -Method POST -Headers @{"Authorization" = "Bearer $($JWT)"} -Body @{"name" = "apple"; "price" = 20} -ContentType "application/json"
if (!$addProductResponse) {
      Write-Host "Failed to add product. Aborting test." -ForegroundColor Red
    return
}
Write-Host ""
# Get products
Write-Host "Getting products..."
$getProductsResponse = Invoke-ApiRequest -Uri "$ADDRESS/get-products" -Method GET -Headers @{"Authorization" = "Bearer $($JWT)"}
if (!$getProductsResponse) {
      Write-Host "Failed to get products. Aborting test." -ForegroundColor Red
    return
}
Write-Host ""
# Add item to cart
Write-Host "Adding apple to cart..."
$addToCartAppleResponse = Invoke-ApiRequest -Uri "$ADDRESS/add-to-cart" -Method POST -Headers @{"Authorization" = "Bearer $($JWT)"} -Body @{"item_name" = "apple"; "quantity" = 2} -ContentType "application/json"
if (!$addToCartAppleResponse) {
       Write-Host "Failed to add apple to cart. Aborting test." -ForegroundColor Red
    return
}
Write-Host ""
# Add banana to cart
Write-Host "Adding banana to cart..."
$addToCartBananaResponse = Invoke-ApiRequest -Uri "$ADDRESS/add-to-cart" -Method POST -Headers @{"Authorization" = "Bearer $($JWT)"} -Body @{"item_name" = "banana"; "quantity" = 2} -ContentType "application/json"
if (!$addToCartBananaResponse) {
      Write-Host "Failed to add banana to cart. Aborting test." -ForegroundColor Red
    return
}
Write-Host ""
# Get cart
Write-Host "Getting cart..."
$cartResponse = Invoke-ApiRequest -Uri "$ADDRESS/get-cart" -Method POST -Headers @{"Authorization" = "Bearer $($JWT)"} -Body @{"username" = "$LOGIN"} -ContentType "application/json"
if (!$cartResponse) {
    Write-Host "Failed to get cart. Aborting test." -ForegroundColor Red
    return
}
Write-Host ""
# Update password
Write-Host "Updating password..."
$updatePasswordResponse = Invoke-ApiRequest -Uri "$ADDRESS/update-password" -Method PUT -Headers @{"Authorization" = "Bearer $($JWT)"} -Body @{"new_password" = "$NEW_PASSWORD"} -ContentType "application/json"
if (!$updatePasswordResponse) {
        Write-Host "Failed to update password. Aborting test." -ForegroundColor Red
    return
}
Write-Host ""
# Delete user
Write-Host "Deleting user..."
$deleteUserResponse = Invoke-ApiRequest -Uri "$ADDRESS/delete-user" -Method DELETE -Headers @{"Authorization" = "Bearer $($JWT)"}
if (!$deleteUserResponse) {
    Write-Host "Failed to delete user. Aborting test." -ForegroundColor Red
    return
}
Write-Host ""
Write-Host "API testing completed." -ForegroundColor Green