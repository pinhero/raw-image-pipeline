import numpy as np
import rawpy
from scipy.ndimage import gaussian_filter, convolve
from PIL import Image
import argparse

class RawProcessor:
    def __init__(self):
        self.params = {
            'denoise': {'sigma_spatial': 1.5, 'sigma_color': 0.05},
            'gamma': {'mid': 0.4},
            'contrast': {'gamma': 1.2, 'contrast': 1.1},
            'sharpen': {'amount': 1.2, 'radius': 0.8}
        }

    def process(self, input_path, output_path):
        """Pipeline principal de traitement d'image RAW"""
        try:
            # Étape 1: Chargement de l'image RAW
            bayer_matrix, black_level, white_level = self._load_raw(input_path)

          # Étape 2: Démosaïçage
            rgb_image = self._demosaic(bayer_matrix, black_level, white_level)

            # Étape 3: Traitements successifs
            processed = self._apply_processing_pipeline(rgb_image)

            # Étape 4: Sauvegarde
            self._save_image(processed, output_path)

            print(f"✅ Traitement réussi : {output_path}")
            return True

        except Exception as e:
            print(f"❌ Erreur : {str(e)}")
            return False

    def _load_raw(self, path):
        """Charge l'image RAW et extrait la matrice Bayer"""
        with rawpy.imread(path) as raw:
            return (
                raw.raw_image_visible.copy(),
                raw.black_level_per_channel[0],
                raw.white_level
            )

    def _demosaic(self, bayer_matrix, black_level, white_level):
        """Démosaïçage personnalisé avec interpolation améliorée"""
        normalized = np.clip((bayer_matrix.astype(np.float32) - black_level) / 
                            (white_level - black_level), 0, 1)
        
        # Masques de couleur
        height, width = normalized.shape
        rgb = np.zeros((height, width, 3))
        rgb[0::2, 0::2, 0] = normalized[0::2, 0::2]  # Rouge
        rgb[1::2, 1::2, 2] = normalized[1::2, 1::2]  # Bleu
        rgb[::, 1::2, 1] = normalized[::, 1::2]      # Vert
        rgb[1::2, ::, 1] = normalized[1::2, ::]      # Vert
        
        # Noyaux d'interpolation
        kernels = [
            np.array([[0.25, 0.5, 0.25], [0.5, 1.0, 0.5], [0.25, 0.5, 0.25]]),
            np.array([[0, 0.25, 0], [0.25, 1.0, 0.25], [0, 0.25, 0]]),
            np.array([[0.25, 0.5, 0.25], [0.5, 1.0, 0.5], [0.25, 0.5, 0.25]])
        ]
        
        for i in range(3):
            kernel = kernels[i] / kernels[i].sum()
            rgb[..., i] = convolve(rgb[..., i], kernel)
            
        return rgb

    def _apply_processing_pipeline(self, image):
        """Applique la chaîne de traitement d'image"""
        # Balance des blancs
        processed = self._white_balance(image)
        
        # Réduction de bruit
        processed = self._denoise(processed)
        
        # Corrections gamma et contraste
        processed = self._gamma_correction(processed)
        processed = self._enhance_contrast(processed)
        
        # Accentuation
        return self._sharpen(processed)

    def _white_balance(self, image):
        balanced = image.copy()
        for c in range(3):
            ref = np.percentile(image[..., c], 98)
            balanced[..., c] /= ref
        return np.clip(balanced, 0, 1)


    def _denoise(self, image):
        """Débruitage bilatéral"""
        denoised = np.zeros_like(image)
        for i in range(3):
            blurred = gaussian_filter(image[..., i], self.params['denoise']['sigma_spatial'])
            diff = np.abs(image[..., i] - blurred)
            mask = np.exp(-(diff**2) / (2 * self.params['denoise']['sigma_color']**2))
            denoised[..., i] = blurred * (1 - mask) + image[..., i] * mask

        return np.clip(denoised, 0, 1)

    def _gamma_correction(self, image):
        """Correction gamma adaptative"""
        mean = np.mean(image)
        gamma = np.log(self.params['gamma']['mid']) / np.log(mean)
        return np.clip(image**gamma, 0, 1)

    def _enhance_contrast(self, image):
        """Amélioration du contraste"""
        luminance = 0.299*image[...,0] + 0.587*image[...,1] + 0.114*image[...,2]
        corrected = np.where(luminance < 0.8, luminance**(1/self.params['contrast']['gamma']), luminance)
        contrasted = 0.5 + self.params['contrast']['contrast'] * (corrected - 0.5)
        ratio = np.clip(contrasted / luminance, 0, 2)
        return np.clip(image * ratio[..., np.newaxis], 0, 1)
  
    def _sharpen(self, image):
        """Accentuation par masque flou"""
        blurred = np.zeros_like(image)
        for i in range(3):
            blurred[..., i] = gaussian_filter(image[..., i], self.params['sharpen']['radius'])
            
        mask = image - blurred
        sharpened = image + mask * self.params['sharpen']['amount']
        return np.clip(sharpened, 0, 1)

    def _save_image(self, image, path):
        """Sauvegarde de l'image finale"""
        Image.fromarray((image * 255).astype('uint8')).save(path, quality=95)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Traite une image RAW")
    parser.add_argument("input", help="Chemin de l'image RAW en entrée")
    parser.add_argument("-o", "--output", default="output.jpg", help="Chemin de sortie")
    
    args = parser.parse_args()
    processor = RawProcessor()
    processor.process(args.input, args.output)
